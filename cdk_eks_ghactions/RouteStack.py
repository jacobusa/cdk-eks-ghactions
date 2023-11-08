from aws_cdk import (
    CfnParameter,
    Stack,
    aws_route53 as route53,
)
from constructs import Construct

from cdk_eks_ghactions.ClusterStack import ClusterStack


class RouteStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        app_domain = CfnParameter(
            self,
            "appDomain",
            type="String",
            description="The name of the hosted zone domain to be created.",
            default="",
        )
        nlb_domain = CfnParameter(
            self,
            "nlbDomain",
            type="String",
            description="The name of the load balancer where cname records need to be made.",
            default="",
        )
        # Create a hosted zone
        hosted_zone = route53.HostedZone(
            self, "hosted-zone", zone_name=app_domain.value_as_string
        )

        # lbDnsName = cluster_stack.cluster.get_ingress_load_balancer_address(
        #     "ingress-nginx",
        #     namespace="ingress-nginx",
        # )
        # route53.ARecord(
        #     self,
        #     "a-record",
        #     zone=hosted_zone,
        #     target=route53.RecordTarget.from_alias(
        #         route53.AliasRecordTargetConfig(
        #             dns_name=lbDnsName, hosted_zone_id=hosted_zone.hosted_zone_id
        #         )
        #     )
        # )

        route53.CnameRecord(
            self,
            "app-cname-record",
            zone=hosted_zone,
            record_name="app",
            domain_name=nlb_domain.value_as_string,
        )
        route53.CnameRecord(
            self,
            "prometheus-cname-record",
            zone=hosted_zone,
            record_name="prometheus",
            domain_name=nlb_domain.value_as_string,
        )
        route53.CnameRecord(
            self,
            "grafana-cname-record",
            zone=hosted_zone,
            record_name="grafana",
            domain_name=nlb_domain.value_as_string,
        )
