from setuptools import setup

setup(
    name="fdcmp",
    version='0.0.3',
    description="Fdc Message Parser",
    author="Fdc",
    author_email="XXXX@sfac.co.kr",
    packages=["bFdc.Eqp", "bFdc.MCP", "bFdc.MP"],
    install_requires=["django-environ"],
)
