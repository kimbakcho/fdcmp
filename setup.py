from setuptools import setup, find_packages

setup(
    name="fdcmp",
    version='0.0.112',
    description="Fdc Message Parser",
    author="Fdc",
    author_email="XXXX@sfac.co.kr",
    packages=find_packages(include=['bFdcAPI*', 'FDCContext', 'ESB*','CapaContext*','ACPContext*']),
    install_requires=["django-environ", "requests", "stomp.py"],
)
