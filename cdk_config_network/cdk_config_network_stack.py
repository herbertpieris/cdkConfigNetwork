from aws_cdk import (
    # Duration,
    aws_ec2 as _ec2,
    RemovalPolicy as _removalpolicy,
    CfnTag as _CfnTag,
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
        vpc = _ec2.CfnVPC(
            self,
            vpcName,
            cidr_block=vpcCidr,
            enable_dns_hostnames=True,
            enable_dns_support=True                                    
        )
        vpc.apply_removal_policy(_removalpolicy.DESTROY)

        #create route table
        route_tablePublic = _ec2.CfnRouteTable(
            self, "RouteTablePublic",
            vpc_id=vpc.attr_vpc_id,

            tags=[_CfnTag(
                key="Name",
                value=vpcName+"-"+"RouteTablePublic"
            )]            
        )
        route_tablePublic.apply_removal_policy(_removalpolicy.DESTROY)

        route_tablePrivate = _ec2.CfnRouteTable(
            self, "RouteTablePrivate",
            vpc_id=vpc.attr_vpc_id,

            tags=[_CfnTag(
                key="Name",
                value=vpcName+"-"+"RouteTablePrivate"
            )]            
        )
        route_tablePrivate.apply_removal_policy(_removalpolicy.DESTROY)        

        #create subnet
        subnetPublic1a = _ec2.CfnSubnet(
            self,
            subnetPublic1aName,
            vpc_id = vpc.attr_vpc_id,
            availability_zone=subnetAZ1a,
            cidr_block=subnetPublic1aCidr            
        )
        subnetPublic1a.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPublic1aRouteTableAssociation = _ec2.CfnSubnetRouteTableAssociation(
            self,
            "subnetPublic1aRouteTableAssociation",
            route_table_id=route_tablePublic.ref,
            subnet_id=subnetPublic1a.attr_subnet_id
        )
        subnetPublic1aRouteTableAssociation.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPublic1b = _ec2.CfnSubnet(
            self,
            subnetPublic1bName,
            vpc_id = vpc.attr_vpc_id,
            availability_zone=subnetAZ1b,
            cidr_block=subnetPublic1bCidr            
        )
        subnetPublic1b.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPublic1bRouteTableAssociation = _ec2.CfnSubnetRouteTableAssociation(
            self,
            "subnetPublic1bRouteTableAssociation",
            route_table_id=route_tablePublic.ref,
            subnet_id=subnetPublic1b.attr_subnet_id
        )
        subnetPublic1bRouteTableAssociation.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPrivate1a01 = _ec2.CfnSubnet(
            self,
            subnetPrivate1aName01,
            vpc_id = vpc.attr_vpc_id,
            availability_zone=subnetAZ1a,
            cidr_block=subnetPrivate1aCidr01            
        )
        subnetPrivate1a01.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPrivate1a01RouteTableAssociation = _ec2.CfnSubnetRouteTableAssociation(
            self,
            "subnetPrivate1a01RouteTableAssociation",
            route_table_id=route_tablePrivate.ref,
            subnet_id=subnetPrivate1a01.attr_subnet_id
        )
        subnetPrivate1a01RouteTableAssociation.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPrivate1b02 = _ec2.CfnSubnet(
            self,
            subnetPrivate1bName02,
            vpc_id = vpc.attr_vpc_id,
            availability_zone=subnetAZ1b,
            cidr_block=subnetPrivatec1bCidr02            
        )
        subnetPrivate1b02.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPrivate1b02RouteTableAssociation = _ec2.CfnSubnetRouteTableAssociation(
            self,
            "subnetPrivate1b02RouteTableAssociation",
            route_table_id=route_tablePrivate.ref,
            subnet_id=subnetPrivate1b02.attr_subnet_id
        )
        subnetPrivate1b02RouteTableAssociation.apply_removal_policy(_removalpolicy.DESTROY)
