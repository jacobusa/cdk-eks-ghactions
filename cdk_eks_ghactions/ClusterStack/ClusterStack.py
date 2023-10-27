import os
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_sns_subscriptions as subs,
    aws_eks as eks,
    lambda_layer_kubectl,
    aws_iam as iam,
    aws_ec2 as ec2,
)
from cdk_eks_ghactions.NetworkStack.NetworkStack import NetworkStack


class ClusterStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, vpc_stack: NetworkStack, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # masters_role = iam.Role(
        #     self,
        #     "eks-admin",
        #     role_name="aws-eks-admin",
        #     assumed_by=iam.CompositePrincipal(
        #         iam.ServicePrincipal(service="eks.amazonaws.com"),
        #         iam.AnyPrincipal(),  # importent, else a SSO user can't assume
        #     ),
        # )
        # masters_role.add_managed_policy(
        #     iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        # )
        # readonly_role = iam.Role(
        #     self,
        #     "eks-readonly",
        #     role_name="aws-eks-readonly",
        #     assumed_by=iam.CompositePrincipal(
        #         iam.ServicePrincipal(service="eks.amazonaws.com"),
        #         iam.AnyPrincipal(),  # importent, else a SSO user can't assume
        #     ),
        # )
        # readonly_role.add_managed_policy(
        #     iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        # )

        cluster = eks.Cluster(
            self,
            "eks-cluster",
            vpc=vpc_stack.vpc,
            # masters_role=masters_role,
            # kubectl_layer=lambda_layer_kubectl.KubectlLayer(self, "kubectl-layer"),
            version=eks.KubernetesVersion.V1_27,
            cluster_name="eks-cluster",
            output_cluster_name=True,
            default_capacity=2,
            default_capacity_instance=ec2.InstanceType.of(
                ec2.InstanceClass.T2, ec2.InstanceSize.MICRO
            ),
            endpoint_access=eks.EndpointAccess.PUBLIC_AND_PRIVATE,
            cluster_logging=[
                eks.ClusterLoggingTypes.API,
                eks.ClusterLoggingTypes.AUTHENTICATOR,
                eks.ClusterLoggingTypes.SCHEDULER,
                eks.ClusterLoggingTypes.AUDIT,
                eks.ClusterLoggingTypes.CONTROLLER_MANAGER,
            ],
        )
        # role_name = 'aws-load-balancer-controller'

        # nodegroup.role.add_to_principal_policy(
        #     iam.PolicyStatement(
        #         actions=[
        #             "ec2:*",
        #             "elasticloadbalancing:*",
        #             "cognito-idp:DescribeUserPoolClient",
        #             "acm:ListCertificates",
        #             "acm:DescribeCertificate",
        #             "iam:ListServerCertificates",
        #             "iam:GetServerCertificate",
        #             "waf-regional:GetWebACL",
        #             "waf-regional:GetWebACLForResource",
        #             "waf-regional:AssociateWebACL",
        #             "waf-regional:DisassociateWebACL",
        #             "wafv2:GetWebACL",
        #             "wafv2:GetWebACLForResource",
        #             "wafv2:AssociateWebACL",
        #             "wafv2:DisassociateWebACL",
        #             "shield:GetSubscriptionState",
        #             "shield:DescribeProtection",
        #             "shield:CreateProtection",
        #             "shield:DeleteProtection"
        #         ],
        #         resources=["*"],
        #     )
        # )

        # eks.HelmChart(
        #     self,
        #     "eks-aws-load-balancer-controller",
        #     cluster=cluster,
        #     chart="aws-load-balancer-controller",
        #     repository="https://aws.github.io/eks-charts",
        #     release="aws-load-balancer-controller",
        #     namespace="kube-system",
        #     values={
        #         "clusterName": cluster.cluster_name,
        #     },
        #     wait=True,
        # )
