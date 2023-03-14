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
        vpcName = "poc-vpc"
        vpcCidr = "192.168.0.0/20"

        # subnet configuration
        subnetConfigurationPublic1a=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Public-1a",                                  
            subnet_type=_ec2.SubnetType.PUBLIC,
        )
        subnetConfigurationPublic1a.apply_removal_policy(_removalpolicy.DESTROY)

        subnetConfigurationPublic1b=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Public-1b",                                  
            subnet_type=_ec2.SubnetType.PUBLIC         
        )
        subnetConfigurationPublic1b.apply_removal_policy(_removalpolicy.DESTROY)

        subnetConfigurationPrivate1a=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-1a",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )
        subnetConfigurationPrivate1a.apply_removal_policy(_removalpolicy.DESTROY)

        subnetConfigurationPrivate1b=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-1b",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )
        subnetConfigurationPrivate1b.apply_removal_policy(_removalpolicy.DESTROY)

        subnetConfigurationPrivateRds1a=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-rds-1a",
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )
        subnetConfigurationPrivateRds1a.apply_removal_policy(_removalpolicy.DESTROY)

        subnetConfigurationPrivateRds1b=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-rds-1b",                             
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )
        subnetConfigurationPrivateRds1b.apply_removal_policy(_removalpolicy.DESTROY)

        subnetConfigurationPrivateGWLBe1a=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-GWLBe-1a",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
        )
        subnetConfigurationPrivateGWLBe1a.apply_removal_policy(_removalpolicy.DESTROY)

        subnetConfigurationPrivateGWLBe1b=_ec2.SubnetConfiguration(
            cidr_mask=24,
            name="Private-GWLBe-1b",                                  
            subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
        )
        subnetConfigurationPrivateGWLBe1b.apply_removal_policy(_removalpolicy.DESTROY)

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
                        ]
        )
        vpc.apply_removal_policy(_removalpolicy.DESTROY)
