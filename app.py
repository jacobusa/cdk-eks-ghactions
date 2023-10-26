#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_eks_ghactions.cdk_eks_ghactions_stack import CdkEksGhactionsStack


app = cdk.App()
CdkEksGhactionsStack(app, "CdkEksGhactionsStack")

app.synth()
