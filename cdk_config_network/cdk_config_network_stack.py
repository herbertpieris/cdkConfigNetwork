from aws_cdk import (
    # Duration,
    aws_ec2 as _ec2,
    RemovalPolicy as _removalpolicy,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkConfigNetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #variable
        vpcName = "poc-vpc"
        vpcCidr = "192.168.0.0/20"
        subnetName = "poc-vpc-1a-public"
        subnetCidr = "192.168.0.0/24"
        OnGWLBeSubnet = True # True or Flase

        # subnet configuration
        subnetConfigurationPublic1a=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Public-1a",                                  
            subnet_type=_ec2.SubnetType.PUBLIC,
        )

        subnetConfigurationPublic1b=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Public-1b",                                  
            subnet_type=_ec2.SubnetType.PUBLIC         
        )

        subnetConfigurationPrivate1a=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-1a",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )

        subnetConfigurationPrivate1b=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-1b",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )

        subnetConfigurationPrivateRds1a=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-rds-1a",
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )

        subnetConfigurationPrivateRds1b=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-rds-1b",                             
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )

        subnetConfigurationPrivateGWLBe1a=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-GWLBe-1a",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
        )

        subnetConfigurationPrivateGWLBe1b=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-GWLBe-1b",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
        )

        #create VPC
        vpc = _ec2.Vpc(self,
                        vpcName,
                        ip_addresses=_ec2.IpAddresses.cidr(vpcCidr),
                        # default_instance_tenancy=_ec2.DefaultInstanceTenancy.DEFAULT,
                        # enable_dns_hostnames=True,
                        # enable_dns_support=True,
                        # # flow_logs=
                        # vpc_name=vpcName,
                        max_azs=0,
                        subnet_configuration= []                        
                        # subnet_configuration= [ 
                        #     subnetConfigurationPublic1a,
                        #     subnetConfigurationPublic1b,
                        #     subnetConfigurationPrivate1a,
                        #     subnetConfigurationPrivate1b,
                        #     subnetConfigurationPrivateRds1a,
                        #     subnetConfigurationPrivateRds1b,
                        #     subnetConfigurationPrivateGWLBe1a,
                        #     subnetConfigurationPrivateGWLBe1b                         
                        # ]
        )
        vpc.apply_removal_policy(_removalpolicy.DESTROY)

        #create subnet
        subnet = _ec2.Subnet(
            self,
            subnetName,
            availability_zone="us-east-1a",
            cidr_block=subnetCidr,
            vpc_id = vpcName,            
            map_public_ip_on_launch=False
        )
        subnet.apply_removal_policy(_removalpolicy.DESTROY)
