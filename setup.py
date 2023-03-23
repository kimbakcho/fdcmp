from setuptools import setup

setup(
    name="fdcmp",
    version='0.0.5',
    description="Fdc Message Parser",
    author="Fdc",
    author_email="XXXX@sfac.co.kr",
    packages=["bFdcAPI.Eqp", "bFdcAPI.MCP", "bFdcAPI.MP", "bFdcAPI", "FDCContext"],
    install_requires=["django-environ"],
)
