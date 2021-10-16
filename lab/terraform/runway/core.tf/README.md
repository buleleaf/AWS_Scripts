
# Core

Deploys a VPC and a (2)Public and (2) Private Subnet for each AZ specified.

Subnets are deployed by calling the subnet module. 

The `for_each` for the module consumes a map of key/value in the form of 
```
Deploys a Internet gateway (IGW) 

Deploys (2) NAT Gateways ; (1) for each AZ (NGW)

Deploys (3) Routing tables : (1) for Public and (2) Private

```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.13 |

## Providers

| Name | Version |
|------|---------|
| aws | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| subnet_group | ./subnet |  |

## Resources

| Name |
|------|
| [aws_availability_zones](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/availability_zones) |
| [aws_internet_gateway](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/internet_gateway) |
| [aws_route_table](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table) |
| [aws_vpc](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc) |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| cidr\_block | VPC Cidr Block | `string` | n/a | yes |
| company | Company Name | `string` | `"nxt"` | no |
| environment | Environment Name | `string` | n/a | yes |
| region | AWS Region | `string` | n/a | yes |
| vpc\_id | VPC Id | `string` | `""` | no |
| vpc\_subnets | Subnet map | `map(any)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| eips\_by\_az | Map of Availiability Zone/Elastic EIP's |
| ngws\_by\_az | Map of Availiability Zone/Nat Gateways |
| pri\_subnet\_by\_az | Map of Availiability Zone/Private Subnets |
| pub\_subnet\_by\_az | Map of Availiability Zone/Public Subnets |
| vpc\_arn | The ARN of the VPC |
| vpc\_id | The ID of the VPC |