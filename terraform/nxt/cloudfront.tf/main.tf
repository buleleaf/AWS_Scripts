locals {
  s3_origin_id      = "nxt-farms-s3origin-dev"
  wix_origin_id     = "nxt-farms-wix-dev"
  wix_origin_domain = "nxt.farm"
}

resource "aws_s3_bucket" "cloudfront_s3bucket" {
  bucket = "${local.s3_origin_id}-static-site"
  acl    = "private"
}

resource "aws_cloudfront_origin_access_identity" "origin_access_identity" {
  comment = "origin accessid for cloudfront"
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions = ["s3:GetObject*", "s3:GetBucket*", "s3:List*"]
    resources = [
      "${aws_s3_bucket.cloudfront_s3bucket.arn}",
      "${aws_s3_bucket.cloudfront_s3bucket.arn}/*"
    ]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.origin_access_identity.iam_arn]
    }
  }
}

# data "terraform_remote_state" "waf" {
#   backend   = "s3"
#   workspace = terraform.workspace
#   config = {
#     bucket = "${var.company}-${var.environment}-${var.region}-terraform-state"
#     region = var.region
#     key    = "waf.tfstate"
#   }
# }

resource "aws_s3_bucket_policy" "cloudfront_s3bucket_policy" {
  bucket = aws_s3_bucket.cloudfront_s3bucket.id
  policy = data.aws_iam_policy_document.s3_policy.json
}

resource "aws_cloudfront_distribution" "cf_distribution" {
  default_root_object = var.default_root_object
  enabled             = true
  price_class         = var.price_class
#   web_acl_id          = data.terraform_remote_state.waf.outputs.waf__acl_arn
  aliases             = ["nxtfarm.com"]

  custom_error_response {
    error_caching_min_ttl = 86400
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
  }

  custom_error_response {
    error_caching_min_ttl = 86400
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    target_origin_id       = local.wix_origin_id
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

  # Wix Origin
  origin {
    domain_name = local.wix_origin_domain
    origin_id   = local.wix_origin_id
    custom_origin_config {
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
      http_port              = 80
      https_port             = 443
    }
  }

  # S3 Origin
  origin {
    domain_name = aws_s3_bucket.cloudfront_s3bucket.bucket_regional_domain_name
    origin_id   = local.s3_origin_id
    origin_path = var.s3_origin_path

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.origin_access_identity.cloudfront_access_identity_path
    }
  }

  # Precedence 0
  ordered_cache_behavior {
    path_pattern     = "/"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = local.wix_origin_id

    forwarded_values {
      query_string = false
      headers      = ["Origin"]
      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 10
    max_ttl                = 60
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }

  # Precedence 1
  ordered_cache_behavior {
    path_pattern     = "/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false
      headers      = ["Origin"]
      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 10
    max_ttl                = 60
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = var.acm_certificate_arn
    minimum_protocol_version = var.minimum_protocol_version
    ssl_support_method       = var.ssl_support_method
  }
}
