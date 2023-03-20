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
        subnetPublic1aName = vpcName + "-1a-public"
        subnetPublic1aCidr = "192.168.0.0/24"
        subnetPublic1bName = vpcName + "-1b-public"
        subnetPublic1bCidr = "192.168.1.0/24"
        subnetPrivate1aName01 = vpcName + "-1a-private-01"
        subnetPrivate1aCidr01 = "192.168.2.0/24"
        subnetPrivate1bName02 = vpcName + "-1b-private-02"
        subnetPrivatec1bCidr02 = "192.168.3.0/24"
        subnetPrivate1aName03 = vpcName + "-1a-private-03"
        subnetPrivate1aCidr03 = "192.168.4.0/24"
        subnetPrivate1bName04 = vpcName + "-1b-private-04"
        subnetPrivatec1bCidr04 = "192.168.5.0/24"
        subnetPrivateGWLB1aName = vpcName + "-1a-private-gwlb"
        subnetPrivateGWLB1aCidr = "192.168.6.0/24"
        subnetPrivateGWLB1bName = vpcName + "-1b-private-gwlb"
        subnetPrivatecGWLB1bCidr = "192.168.7.0/24"                                
        subnetAZ1a = "us-east-1a"
        subnetAZ1b = "us-east-1b"
        OnGWLBeSubnet = True # True or Flase

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

        #create route table
        route_table1 = _ec2.CfnRouteTable(
            self, "MyRouteTable",
            vpc_id=vpc.vpc_id        
        )
        route_table1.apply_removal_policy(_removalpolicy.DESTROY)

        #create subnet
        subnetPublic1a = _ec2.Subnet(
            self,
            subnetPublic1aName,
            availability_zone=subnetAZ1a,
            cidr_block=subnetPublic1aCidr,
            vpc_id = vpc.vpc_id,            
            map_public_ip_on_launch=False
        )
        subnetPublic1a.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPublic1aAttr = _ec2.SubnetAttributes(
            subnet_id = subnetPublic1a.subnet_id,
            route_table_id=route_table1.attr_route_table_id
        )

        subnetPublic1b = _ec2.Subnet(
            self,
            subnetPublic1bName,
            availability_zone=subnetAZ1b,
            cidr_block=subnetPublic1bCidr,
            vpc_id = vpc.vpc_id,            
            map_public_ip_on_launch=False
        )
        subnetPublic1b.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPrivate1a01 = _ec2.Subnet(
            self,
            subnetPrivate1aName01,
            availability_zone=subnetAZ1a,
            cidr_block=subnetPrivate1aCidr01,
            vpc_id = vpc.vpc_id,            
            map_public_ip_on_launch=False
        )
        subnetPrivate1a01.apply_removal_policy(_removalpolicy.DESTROY)              
