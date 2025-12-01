from setuptools import setup, find_packages

setup(
    name="extract_load_s3",
    version="1.0.2",
    description="Unified data ingestion framework to move datasets from SFTP/Oracle/Postgres/Snowflake to S3.",
    author="Hasan",
    author_email="hasanali242424@gmail.com",
    url="https://github.com/hasannasrul/extract-loads3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "boto3>=1.20",
        "paramiko>=3.0",
    ],
    python_requires=">=3.9",
    license="MIT",
)
