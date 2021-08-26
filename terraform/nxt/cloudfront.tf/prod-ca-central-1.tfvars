region = "ca-central-1"
# The object that you want CloudFront to return (for example, index.html) when an end user requests the root URL.
default_root_object = "index.html"
company             = "nxt"
environment         = "prod"
price_class         = "PriceClass_All"
s3_origin_path      = "/build"
wix_origin_path     = "/"

# Certificate Config
acm_certificate_arn      = "arn:aws:acm:us-east-1:654770434413:certificate/51493e98-57d1-463e-8ba6-e3b1a8d1c9d4"
minimum_protocol_version = "TLSv1.2_2018"
ssl_support_method       = "sni-only"
