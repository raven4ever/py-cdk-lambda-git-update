from aws_cdk import (
    core,
    aws_lambda as lmdb,
    aws_apigateway as apigw,
)


class LambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # API GW definition
        api = apigw.RestApi(self, 'API-GW')

        # Create function
        updateFunction = lmdb.Function(self, 'Github-Update-Function',
                                       function_name='Github-Update-Function',
                                       runtime=lmdb.Runtime.PYTHON_3_8,
                                       code=lmdb.Code.from_asset(path='lambda/github_update'),
                                       handler='main.handler')

        gwIntegration = apigw.LambdaIntegration(updateFunction)
        api.root.add_resource('update').add_method('POST', gwIntegration)
