from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc_name = construct_id
        self.construct_id = construct_id
        self.__create_vpc()

    def __create_vpc(self):
        self.vpc: ec2.Vpc = ec2.Vpc(
            self,
            self.construct_id,
            vpc_name=self.vpc_name,
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC, name="public", cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="private",
                    cidr_mask=24,
                ),
                # ec2.SubnetConfiguration(
                #     subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                #     name="RDS",
                #     cidr_mask=20,
                # ),
            ],
            nat_gateways=1,
        )
