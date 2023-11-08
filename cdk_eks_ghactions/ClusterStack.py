import os
from constructs import Construct
from aws_cdk import Stack, aws_eks as eks, aws_iam as iam, aws_ec2 as ec2, CfnOutput
from cdk_eks_ghactions.NetworkStack import NetworkStack
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer


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
        #         iam.AnyPrincipal()
        #     ),
        # )
        # Create an IAM Role to be assumed by admins
        self.masters_role = iam.Role(
            self,
            os.getenv("MASTERS_ROLE_NAME"),
            assumed_by=iam.AccountRootPrincipal(),
            role_name=os.getenv("MASTERS_ROLE_NAME"),
        )
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
            os.getenv("CLUSTER_NAME"),
            vpc=vpc_stack.vpc,
            masters_role=self.masters_role,
            version=eks.KubernetesVersion.V1_27,
            cluster_name=os.getenv("CLUSTER_NAME"),
            output_cluster_name=True,
            output_config_command=True,
            default_capacity=1,
            # kubectl_layer=KubectlV24Layer(self, "KubectlV24Layer"),
            output_masters_role_arn=True,
            # default_capacity_instance=ec2.InstanceType.of(
            #     ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM
            # ),
            endpoint_access=eks.EndpointAccess.PUBLIC_AND_PRIVATE,
            cluster_logging=[
                eks.ClusterLoggingTypes.API,
                eks.ClusterLoggingTypes.AUTHENTICATOR,
                eks.ClusterLoggingTypes.SCHEDULER,
                eks.ClusterLoggingTypes.AUDIT,
                eks.ClusterLoggingTypes.CONTROLLER_MANAGER,
            ],
        )

        # ingress_controller_release_name = "ingress-controller"
        # nginxIngressChart = eks.HelmChart(
        #     self,
        #     "nginx-ingress-chart",
        #     cluster=cluster,
        #     repository="https://helm.nginx.com/stable",
        #     chart="nginx-ingress",
        #     release="nginx-ingress",
        # )
        # alb_address = eks.KubernetesObjectValue(
        #     self,
        #     "elbAddress",
        #     cluster=cluster,
        #     object_type="Service",
        #     object_name=f"{ingress_controller_release_name}-nginx-ingress",
        #     json_path=".status.loadBalancer.ingress[0].hostname",
        # )
        # self.alb_domain = alb_address.value
        # CfnOutput(self, "alb-domain", value=alb_address.value)

        # nginxIngressChart = eks.HelmChart(
        #     self,
        #     "nginx-ingress-chart",
        #     cluster=cluster,
        #     repository="https://helm.nginx.com/stable",
        #     chart="nginx-ingress",
        #     release="nginx-ingress",
        #     values=
        # )
        # cluster.open_id_connect_provider.
        # kubectlProvider = eks.KubectlProvider

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
