from setuptools import setup, find_packages

setup(
    name="fdcmp",
    version='0.0.69',
    description="Fdc Message Parser",
    author="Fdc",
    author_email="XXXX@sfac.co.kr",
    packages=find_packages(include=['bFdcAPI*', 'FDCContext', 'ESB*','CapaContext*','ACPContext*']),
    install_requires=["django-environ", "requests", "stomp.py", "pymongo==3.12.1"],
)
