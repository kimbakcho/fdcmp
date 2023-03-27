from setuptools import setup, find_packages

setup(
    name="fdcmp",
    version='0.0.13',
    description="Fdc Message Parser",
    author="Fdc",
    author_email="XXXX@sfac.co.kr",
    packages=find_packages(include=['bFdcAPI*', 'FDCContext']),
    install_requires=["django-environ", "requests"],
)
