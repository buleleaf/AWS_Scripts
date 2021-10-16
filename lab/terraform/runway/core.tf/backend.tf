terraform {
  backend "s3" {
    key = "core.tfstate"
  }
}
