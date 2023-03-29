from aws_cdk import (
    # Duration,
    aws_ec2 as _ec2,
    aws_logs as _log,
    aws_iam as _iam,
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
        ## VPC
        vpcName = "poc-vpc"
        vpcCidr = "192.168.0.0/20"
        
        ## IGW
        vpcIgwName = "poc-vpc-igw"

        ## Public subnet
        subnetPublic1aName = vpcName + "-1a-public"
        subnetPublic1aCidr = "192.168.0.0/24"
        subnetPublic1bName = vpcName + "-1b-public"
        subnetPublic1bCidr = "192.168.1.0/24"

        ## Private subnet
        subnetPrivate1aName01 = vpcName + "-1a-private-01"
        subnetPrivate1aCidr01 = "192.168.2.0/24"
        subnetPrivate1bName02 = vpcName + "-1b-private-02"
        subnetPrivatec1bCidr02 = "192.168.3.0/24"
        subnetPrivate1aName03 = vpcName + "-1a-private-03"
        subnetPrivate1aCidr03 = "192.168.4.0/24"
        subnetPrivate1bName04 = vpcName + "-1b-private-04"
        subnetPrivatec1bCidr04 = "192.168.5.0/24"

        ## Private GWLB subnet 
        subnetPrivateGWLB1aName = vpcName + "-1a-private-gwlb"
        subnetPrivateGWLB1aCidr = "192.168.6.0/24"
        subnetPrivateGWLB1bName = vpcName + "-1b-private-gwlb"
        subnetPrivateGWLB1bCidr = "192.168.7.0/24"                                

        ## vpc flow log
        vpcFlowLogName = vpcName + "-flowlog"
        logGroupName = 'VPCFlowLog'
        logDestinationType="s3" # cloud-watch-logs | s3
        logDestinationS3Arn="arn:aws:s3:::herb-assets"

        ## AZs
        subnetAZ1a = "us-east-1a"
        subnetAZ1b = "us-east-1b"

        ## condition GWLB
        OnGWLBeSubnet = True # True or Flase

        ## condition VPCFlowLog
        OnFLowLog = True # True or Flase

        ## condition NatGateway
        OnNatGateway = True # True or Flase        

        #create VPC
        vpc = _ec2.CfnVPC(
            self,
            vpcName,
            cidr_block=vpcCidr,
            enable_dns_hostnames=True,
            enable_dns_support=True,

            tags=[_CfnTag(
                key="Name",
                value=vpcName
            )]                   
        )
        vpc.apply_removal_policy(_removalpolicy.DESTROY)

        #create VPC IGW
        vpcIgw = _ec2.CfnInternetGateway(
            self,
            vpcIgwName,
            tags=[_CfnTag(
                key="Name",
                value=vpcName
            )]                   
        )
        vpcIgw.apply_removal_policy(_removalpolicy.DESTROY)

        #IGW attached to VPC
        vpcIGWAttachment = _ec2.CfnVPCGatewayAttachment(self, "vpcIGWAttachment",
            vpc_id=vpc.attr_vpc_id,

            # the properties below are optional
            internet_gateway_id=vpcIgw.attr_internet_gateway_id
        )
        vpcIGWAttachment.apply_removal_policy(_removalpolicy.DESTROY)

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
        ## public
        subnetPublic1a = _ec2.CfnSubnet(
            self,
            subnetPublic1aName,
            vpc_id = vpc.attr_vpc_id,
            availability_zone=subnetAZ1a,
            cidr_block=subnetPublic1aCidr,

            tags=[_CfnTag(
                key="Name",
                value=vpcName+"-"+"subnetPublic1a"
            )]
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
            cidr_block=subnetPublic1bCidr,

            tags=[_CfnTag(
                key="Name",
                value=vpcName+"-"+"subnetPublic1b"
            )]            
        )
        subnetPublic1b.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPublic1bRouteTableAssociation = _ec2.CfnSubnetRouteTableAssociation(
            self,
            "subnetPublic1bRouteTableAssociation",
            route_table_id=route_tablePublic.ref,
            subnet_id=subnetPublic1b.attr_subnet_id
        )
        subnetPublic1bRouteTableAssociation.apply_removal_policy(_removalpolicy.DESTROY)

        ## private
        subnetPrivate1a01 = _ec2.CfnSubnet(
            self,
            subnetPrivate1aName01,
            vpc_id = vpc.attr_vpc_id,
            availability_zone=subnetAZ1a,
            cidr_block=subnetPrivate1aCidr01,

            tags=[_CfnTag(
                key="Name",
                value=vpcName+"-"+"subnetPrivate1a01"
            )]
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
            cidr_block=subnetPrivatec1bCidr02,

            tags=[_CfnTag(
                key="Name",
                value=vpcName+"-"+"subnetPrivate1b02"
            )]            
        )
        subnetPrivate1b02.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPrivate1b02RouteTableAssociation = _ec2.CfnSubnetRouteTableAssociation(
            self,
            "subnetPrivate1b02RouteTableAssociation",
            route_table_id=route_tablePrivate.ref,
            subnet_id=subnetPrivate1b02.attr_subnet_id
        )
        subnetPrivate1b02RouteTableAssociation.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPrivate1a03 = _ec2.CfnSubnet(
            self,
            subnetPrivate1aName03,
            vpc_id = vpc.attr_vpc_id,
            availability_zone=subnetAZ1a,
            cidr_block=subnetPrivate1aCidr03,

            tags=[_CfnTag(
                key="Name",
                value=vpcName+"-"+"subnetPrivate1a03"
            )]
        )
        subnetPrivate1a03.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPrivate1a03RouteTableAssociation = _ec2.CfnSubnetRouteTableAssociation(
            self,
            "subnetPrivate1a03RouteTableAssociation",
            route_table_id=route_tablePrivate.ref,
            subnet_id=subnetPrivate1a03.attr_subnet_id
        )
        subnetPrivate1a03RouteTableAssociation.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPrivate1b04 = _ec2.CfnSubnet(
            self,
            subnetPrivate1bName04,
            vpc_id = vpc.attr_vpc_id,
            availability_zone=subnetAZ1b,
            cidr_block=subnetPrivatec1bCidr04,

            tags=[_CfnTag(
                key="Name",
                value=vpcName+"-"+"subnetPrivate1b04"
            )]            
        )
        subnetPrivate1b04.apply_removal_policy(_removalpolicy.DESTROY)

        subnetPrivate1b04RouteTableAssociation = _ec2.CfnSubnetRouteTableAssociation(
            self,
            "subnetPrivate1b04RouteTableAssociation",
            route_table_id=route_tablePrivate.ref,
            subnet_id=subnetPrivate1b04.attr_subnet_id
        )
        subnetPrivate1b04RouteTableAssociation.apply_removal_policy(_removalpolicy.DESTROY)

        ## private gwlb
        if OnGWLBeSubnet:
            subnetPrivateGWLB1a = _ec2.CfnSubnet(
                self,
                subnetPrivateGWLB1aName,
                vpc_id = vpc.attr_vpc_id,
                availability_zone=subnetAZ1a,
                cidr_block=subnetPrivateGWLB1aCidr,

                tags=[_CfnTag(
                    key="Name",
                    value=vpcName+"-"+"subnetPrivateGWLB1a"
                )]            
            )
            subnetPrivateGWLB1a.apply_removal_policy(_removalpolicy.DESTROY)

            subnetPrivateGWLB1aRouteTableAssociation = _ec2.CfnSubnetRouteTableAssociation(
                self,
                "subnetPrivateGWLB1aRouteTableAssociation",
                route_table_id=route_tablePrivate.ref,
                subnet_id=subnetPrivateGWLB1a.attr_subnet_id
            )
            subnetPrivateGWLB1aRouteTableAssociation.apply_removal_policy(_removalpolicy.DESTROY)

            subnetPrivateGWLB1b = _ec2.CfnSubnet(
                self,
                subnetPrivateGWLB1bName,
                vpc_id = vpc.attr_vpc_id,
                availability_zone=subnetAZ1b,
                cidr_block=subnetPrivateGWLB1bCidr,

                tags=[_CfnTag(
                    key="Name",
                    value=vpcName+"-"+"subnetPrivateGWLB1b"
                )]            
            )
            subnetPrivateGWLB1b.apply_removal_policy(_removalpolicy.DESTROY)

            subnetPrivateGWLB1bRouteTableAssociation = _ec2.CfnSubnetRouteTableAssociation(
                self,
                "subnetPrivateGWLB1bRouteTableAssociation",
                route_table_id=route_tablePrivate.ref,
                subnet_id=subnetPrivateGWLB1b.attr_subnet_id
            )
            subnetPrivateGWLB1bRouteTableAssociation.apply_removal_policy(_removalpolicy.DESTROY)

        if OnNatGateway:
            #IGW attached to VPC
            natGateway = _ec2.CfnNatGateway(
                self,
                "natGateway",
                subnet_id=subnetPublic1a.attr_subnet_id

            )
            natGateway.apply_removal_policy(_removalpolicy.DESTROY)

        #vpc flow log        
        if OnFLowLog:
            if logDestinationType=='cloud-watch-logs':
                # policy statement
                vpcFlowLogIAMPolicyStatement = _iam.PolicyStatement(
                    actions=[
                    'logs:CreateLogStream',
                    'logs:PutLogEvents',
                    'logs:DescribeLogGroups',
                    'logs:DescribeLogStreams'
                    ],
                    resources=["*"]
                )

                # managed policy
                vpcFlowLogIAMManagedPolicy = _iam.ManagedPolicy(
                        self,
                        "Flow-Logs-Policy",
                        description="iam policy for Flow Log",
                        managed_policy_name="Flow-Logs-Policy"
                    )
                vpcFlowLogIAMManagedPolicy.add_statements(vpcFlowLogIAMPolicyStatement)
                vpcFlowLogIAMManagedPolicy.apply_removal_policy(_removalpolicy.DESTROY)

                # role
                vpcFlowLogIAMRole = _iam.Role(
                        self,
                        "Flow-Logs-Role",
                        assumed_by=_iam.ServicePrincipal("vpc-flow-logs.amazonaws.com"),
                        description="iam role for Flow Log",
                        role_name="Flow-Logs-Role"
                    )
                vpcFlowLogIAMRole.add_managed_policy(vpcFlowLogIAMManagedPolicy)
                vpcFlowLogIAMRole.apply_removal_policy(_removalpolicy.DESTROY)            

                # Log group
                vpcFlowLogGroup = _log.LogGroup(
                    self,
                    logGroupName,
                    log_group_name=logGroupName
                )
                vpcFlowLogGroup.apply_removal_policy(_removalpolicy.DESTROY)

                # Flow Log
                vpcFlowLog = _ec2.CfnFlowLog(
                    self, 
                    vpcFlowLogName,
                    resource_id=vpc.attr_vpc_id,
                    resource_type="VPC",

                    # the properties below are optional
                    deliver_logs_permission_arn=vpcFlowLogIAMRole.role_arn,
                    log_destination=vpcFlowLogGroup.log_group_arn,
                    log_destination_type=logDestinationType,
                    # log_group_name=logGroupName,
                    # max_aggregation_interval=123,

                    tags=[_CfnTag(
                        key="Name",
                        value=vpcName+"-"+"vpcFlowLog"
                    )],
                    traffic_type="ALL"
                )
                vpcFlowLog.apply_removal_policy(_removalpolicy.DESTROY)
            elif logDestinationType=='s3':
                # Flow Log
                vpcFlowLog = _ec2.CfnFlowLog(
                    self, 
                    vpcFlowLogName,
                    resource_id=vpc.attr_vpc_id,
                    resource_type="VPC",

                    # the properties below are optional
                    log_destination=logDestinationS3Arn,
                    log_destination_type=logDestinationType,
                    # log_group_name=logGroupName,
                    # max_aggregation_interval=123,

                    tags=[_CfnTag(
                        key="Name",
                        value=vpcName+"-"+"vpcFlowLog"
                    )],
                    traffic_type="ALL"
                )
                vpcFlowLog.apply_removal_policy(_removalpolicy.DESTROY)                