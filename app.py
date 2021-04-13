from aws_cdk import core

from infra_stack.lambda_infra import LambdaStack

app = core.App()
LambdaStack(app, "GitUpdateStack")

app.synth()
