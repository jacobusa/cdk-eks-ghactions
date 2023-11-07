import os
from constructs import Construct
from aws_cdk import (
    Stack,
    Environment,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
)
from cdk_eks_ghactions.ClusterStack import ClusterStack
from cdk_eks_ghactions.NetworkStack import NetworkStack

# from cdk_eks_ghactions import NetworkStack


class CdkEksGhactionsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc_stack = NetworkStack(
            self,
            "vpc-stack",
            env=Environment(
                account=os.getenv("AWS_ACCOUNT_ID"), region=os.environ.get("AWS_REGION")
            ),
        )

        cluster_stack = ClusterStack(
            self,
            "cluster-stack",
            vpc_stack,
            env=Environment(
                account=os.getenv("AWS_ACCOUNT_ID"), region=os.environ.get("AWS_REGION")
            ),
        )
        # route53.ARecord(
        #     self,
        #     "a-record",
        #     zone=vpc_stack.hosted_zone,
        #     target=route53.RecordTarget.from_alias(
        #         route53_targets.LoadBalancerTarget(cluster_stack.alb_domain)
        #     ),
        # )

        # cluster_stack = eks.Cluster(
        #     self,
        #     "eks-cluster",
        #     vpc=vpc_stack.vpc,
        #     masters_role=masters_role,
        #     kubectl_layer=lambda_layer_kubectl.KubectlLayer(self, "kubectl-layer"),
        #     version=eks.KubernetesVersion.V1_27,
        #     default_capacity=2,
        #     cluster_logging=[
        #         eks.ClusterLoggingTypes.API,
        #         eks.ClusterLoggingTypes.AUTHENTICATOR,
        #         eks.ClusterLoggingTypes.SCHEDULER,
        #         eks.ClusterLoggingTypes.AUDIT,
        #         eks.ClusterLoggingTypes.CONTROLLER_MANAGER,
        #     ],
        # )


# queue = sqs.Queue(
#     self,
#     "CdkEksGhactionsQueue",
#     visibility_timeout=Duration.seconds(300),
# )

# topic = sns.Topic(self, "CdkEksGhactionsTopic")

#  lambdaFunction = _lambda.Function(
#     self,
#     "lambda",
#     runtime=_lambda.Runtime.NODEJS_10_X,
# )
# topic.add_subscription(subs.SqsSubscription(queue))
