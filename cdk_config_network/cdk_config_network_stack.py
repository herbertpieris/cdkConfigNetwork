from aws_cdk import (
    # Duration,
    aws_ec2 as _ec2,
    Tags as _tags,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkConfigNetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        vpcName = "poc-vpc"
        vpcCidr = "192.168.0.0/20"

        # subnet configuration
        subnetConfigurationPublic1=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="PUBLIC1",                                  
            subnet_type=_ec2.SubnetType.PUBLIC,
        )
        _tags.of(subnetConfigurationPublic1).add("StackType", "TheBest")

        subnetConfigurationPublic2=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="PUBLIC2",                                  
            subnet_type=_ec2.SubnetType.PUBLIC         
        )        
        subnetConfigurationPrivate1=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private1",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )
        subnetConfigurationPrivate2=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private2",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )
        subnetConfigurationPrivate3=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private3",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )
        subnetConfigurationPrivate4=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private4",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )
        subnetConfigurationGWLBe1=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="GWLBe1",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
        )
        subnetConfigurationGWLBe2=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="GWLBe2",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
        )                                      

        #create VPC
        vpc = _ec2.Vpc(self,
                        vpcName,
                        ip_addresses=_ec2.IpAddresses.cidr(vpcCidr),
                        default_instance_tenancy=_ec2.DefaultInstanceTenancy.DEFAULT,
                        enable_dns_hostnames=True,
                        enable_dns_support=True,
                        # flow_logs=
                        vpc_name=vpcName,
                        max_azs=2,
                        subnet_configuration= [ 
                            subnetConfigurationPublic1,
                            subnetConfigurationPublic2,
                            subnetConfigurationPrivate1,
                            subnetConfigurationPrivate2,
                            subnetConfigurationPrivate3,
                            subnetConfigurationPrivate4,
                            subnetConfigurationGWLBe1,
                            subnetConfigurationGWLBe2
                            # {
                            #     # cidr_mask=28,
                            #     name="rds", 
                            #     subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
                            # }                           
                        ]
        )
