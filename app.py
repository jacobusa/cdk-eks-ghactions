#!/usr/bin/env python3

import os
import aws_cdk as cdk

from dotenv import load_dotenv
from cdk_eks_ghactions.NetworkStack import NetworkStack
from cdk_eks_ghactions.cdk_eks_ghactions_stack import CdkEksGhactionsStack


load_dotenv()


app = cdk.App()
CdkEksGhactionsStack(
    app,
    "cdk-eks-ghactions-stack",
    env=cdk.Environment(
        account=os.getenv("AWS_ACCOUNT_ID"), region=os.environ.get("AWS_REGION")
    ),
)

app.synth()
