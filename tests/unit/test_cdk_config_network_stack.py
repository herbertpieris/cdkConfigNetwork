import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_config_network.cdk_config_network_stack import CdkConfigNetworkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_config_network/cdk_config_network_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkConfigNetworkStack(app, "cdk-config-network")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
