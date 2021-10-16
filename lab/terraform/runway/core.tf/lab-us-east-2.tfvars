region      = "us-east-2"
environment = "lab"
cidr_block  = "172.25.0.0/16"
vpc_subnets = {
  us-east-2a = {
    public  = "172.25.10.0/24",
    private = "172.25.20.0/24"
  },
  us-east-2b = {
    public  = "172.25.12.0/24",
    private = "172.25.22.0/24"
  }
}

