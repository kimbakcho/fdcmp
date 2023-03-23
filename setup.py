from setuptools import setup, find_packages

setup(
    name="fdcmp",
    version='0.0.6',
    description="Fdc Message Parser",
    author="Fdc",
    author_email="XXXX@sfac.co.kr",
    packages=find_packages(where='fdcmp', include=['bFdcAPI*', 'FDCContext']),
    install_requires=["django-environ"],
)
