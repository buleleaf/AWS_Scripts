terraform {
  backend "s3" {
    key = "packer-poc.tfstate"
  }
}
