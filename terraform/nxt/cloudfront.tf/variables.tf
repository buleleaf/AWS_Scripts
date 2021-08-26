variable "environment" {
  default     = "prod"
  description = "Environment to launch into"
}

variable "region" {
  description = "Region for the config to be deployed in."
  type        = string
}

variable "company" {
  type        = string
  description = "Company Name"
  default     = "nxt"
}

variable "default_root_object" {
  description = "The object that you want CloudFront to return (for example, index.html) when an end user requests the root URL."
  type        = string
  default     = ""
}

variable "price_class" {
  description = "The price class for this distribution. One of PriceClass_All, PriceClass_200, PriceClass_100."
  type        = string
  default     = "PriceClass_100"

}
variable "acm_certificate_arn" {
  description = "The ARN of the AWS Certificate Manager certificate that you wish to use with this distribution. Specify this, cloudfront_default_certificate, or iam_certificate_id. The ACM certificate must be in US-EAST-1."
  type        = string
  default     = ""
}

variable "minimum_protocol_version" {
  description = "The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. See https://www.terraform.io/docs/providers/aws/r/cloudfront_distribution.html#minimum_protocol_version"
  type        = string
  default     = "TLSv1.2_2018"
}

variable "ssl_support_method" {
  description = "Specifies how you want CloudFront to serve HTTPS requests. One of vip or sni-only. Required if you specify acm_certificate_arn or iam_certificate_id. NOTE: vip causes CloudFront to use a dedicated IP address and may incur extra charges."
  type        = string
  default     = "sni-only"
}

variable "s3_origin_path" {
  description = "A directory in your Amazon S3 bucket or your custom origin"
  type        = string
  default     = ""
}
