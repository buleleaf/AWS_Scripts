# Core Stack Use

1. Allocate [VPC & VPN subnets](https://nbdevs.atlassian.net/wiki/display/SG/Infrastructure+Subnets)
2. Update the sample VPN wrapper cookbook for the customer:
    * Rename `cookbooks/CUSTOMERNAME_vpn`, replacing the name to match the `customername` stacker environment variable (e.g. `moestavern_vpn`)
    * Edit the cookbook's metadata.rb file and update the cookbook name to match the new directory name
3. Setup your AWS profile in your terminal (e.g. sturdy-sso)
4. Deploy the buckets/vpnip stacks:
    * `cd sturdy-stacker-core`
    * `stacker build -i -r REGIONNAME ../../environments/common.env bootstrap.yaml`
5. Deploy the full core stack:
    * `stacker build -i -r REGIONNAME ../../environments/common.env core.yaml`
6. See [OpenVPN LDAP setup](https://nbdevs.atlassian.net/wiki/display/SG/OpenVPN+LDAP+setup) on the wiki ('Non-Sing Setup' section). Follow its first 2 steps to:
    * Allow access from the VPN EIP (IP address is listed in EIP stack Outputs)
    * Add a user group of the form `sturdy-vpn-CUSTOMERNAME`
        * Add devops team members to this group to allow them access to the VPN
    * Note: a bind account (created on the command line) is *NOT* required -- user accounts will directly bind to the ldap server to verify their credentials
7. Once the instance has completed its initial configuration, download the OpenVPN connection file and distribute it for access. E.g.: `aws s3 cp s3://ARTIFACTBUCKET/common/vpnservers/client.ovpn ./`

## Updating VPN Server Configuration (Standalone)

1. Update the vpn cookbook
2. Generate a new archive via `berks package`
3. Upload it to the S3 folder as noted above
    * Instances will use the highest-numbered package found in the folder, so multiple cookbook packages can technically coexist during testing/transitions.
4. Perform one of the following methods of deploying the updated config

### Instance Rebuild

A complete rebuild of the instance can be initiated by terminating it (**NOTE** this will interrupt VPN service for ~5 min).

### SSM

Minor changes to the instance Chef config can be performed via EC2 SSM Run Command (SSM -> Managed Instances -> "Run a Command", then select the core-chefrun-docs-Linux command document)

## Specifying a Custom chef-client Recipe

Set `vpn_chef_client_runlist` in your environment (e.g. `vpn_chef_client_runlist: recipe[customer_openvpn::default]`) to override the default `CUSTOMERNAME_vpn` cookbook name.

## Availability Zone Offset
Set `vpc_az_offset` in your environment with an integer to override which availability zones are used
* The AzOffset is added to the Select count for choosing AZs
    * Default AZs us-east-1a, us-east-1b
    * If AzOffset is 1 AZs are us-east-1b, us-east-1c

## Specifying a Custom Stacker Bucket

The [Stacker S3 bucket](https://stacker.readthedocs.io/en/latest/config.html#s3-bucket) can be overridden by setting `stacker_bucket_name` in your environment.
