#!/usr/bin/env python3
import os
from aws_cdk import App, Environment
from dotenv import load_dotenv
from cdk_eks_ghactions.NetworkStack import NetworkStack
from cdk_eks_ghactions.ClusterStack import ClusterStack
from cdk_eks_ghactions.NetworkStack import NetworkStack


load_dotenv()


app = App()
# CdkEksGhactionsStack(
#     app,
#     "cdk-eks-ghactions-stack",
#     env=cdk.Environment(
#         account=os.getenv("AWS_ACCOUNT_ID"), region=os.environ.get("AWS_REGION")
#     ),
# )
vpc_stack = NetworkStack(
    app,
    "vpc-stack",
    env=Environment(
        account=os.getenv("AWS_ACCOUNT_ID"), region=os.environ.get("AWS_REGION")
    ),
)

cluster_stack = ClusterStack(
    app,
    "cluster-stack",
    vpc_stack,
    env=Environment(
        account=os.getenv("AWS_ACCOUNT_ID"), region=os.environ.get("AWS_REGION")
    ),
)

app.synth()
