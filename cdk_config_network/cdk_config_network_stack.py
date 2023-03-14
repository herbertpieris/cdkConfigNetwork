from aws_cdk import (
    # Duration,
    aws_ec2 as _ec2,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkConfigNetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        vpcName = "japfa-poc-vpc"
        vpcCidr = "192.168.0.0/20"

        #create VPC
        vpc = _ec2.Vpc(self,
                        vpcName,
                        ip_addresses=_ec2.IpAddresses.cidr(vpcCidr),
                        default_instance_tenancy=_ec2.DefaultInstanceTenancy.DEFAULT,
                        enable_dns_hostnames=True,
                        enable_dns_support=True,
                        # flow_logs=
                        vpc_name=vpcName,
                        max_azs=2                        
        )
