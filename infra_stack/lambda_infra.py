from aws_cdk import (
    core,
    aws_lambda as lmdb,
    aws_apigateway as apigw,
)
from aws_cdk.aws_lambda_python import PythonFunction


class LambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # API GW definition
        api = apigw.RestApi(self, 'API-GW')

        # Create function
        updateFunction = PythonFunction(self, 'Github-Update-Function',
                                        function_name='Github-Update-Function',
                                        runtime=lmdb.Runtime.PYTHON_3_8,
                                        index='main.py',
                                        handler='lambda_handler',
                                        entry='lambda/github_update',
                                        current_version_options=lmdb.VersionOptions(
                                            removal_policy=core.RemovalPolicy.RETAIN)
                                        )

        dev = lmdb.Alias(self, 'development', alias_name='development', version=updateFunction.current_version)

        gwIntegration = apigw.LambdaIntegration(updateFunction)
        api.root.add_resource('update').add_method('POST', gwIntegration)
