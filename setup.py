import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="infra_stack",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "infra_stack"},
    packages=setuptools.find_packages(where="infra_stack"),

    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws_lambda",
        "aws-cdk.aws_apigateway"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",
    ],
)
