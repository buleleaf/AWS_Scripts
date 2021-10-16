region      = "us-east-2"
environment = "dahlin-lab"
cidr_block  = "192.168.0.0/16"
tgw_id      = "tgw-07eb193a8c616193d"

vpc_subnets = {
  us-east-2a = {
    tgw_attached = {
      tgw-test = "192.168.0.0/24"
    }
    private = {
      bits   = "192.168.1.0/24"
      devops = "192.168.2.0/24"
    }
    public = {}
  }
  us-east-2b = {
    tgw_attached = {
      tgw-test = "192.168.4.0/24"
    }
    private = {
      bits   = "192.168.5.0/24"
      devops = "192.168.6.0/24"
    }
    public = {}
  }
}

tags = {
  owner                = "sharednetwork-nonprod"
  environment          = "sharednetwork-nonprod"
  purpose              = "infrastructure"
  backup-plan-schedule = "not-applicable"
  update-schedule      = "not-applicable"
  uptime-scheduler     = "all"
  created-by           = "terraform"
}
