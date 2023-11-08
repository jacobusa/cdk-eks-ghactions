from aws_cdk import (
    CfnParameter,
    Stack,
    aws_route53 as route53,
)
from constructs import Construct


class RouteStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        nlb_domain = CfnParameter(
            self,
            "nlb_domain",
            type="String",
            description="The name of the load balancer where cname records need to be made.",
            default="",
        )
        # Create a hosted zone
        hosted_zone = route53.HostedZone(
            self, "hosted-zone", zone_name="justadomain.xyz"
        )

        #  Create a CNAME record
        route53.CnameRecord(
            self,
            "@-cname-record",
            zone=hosted_zone,
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
