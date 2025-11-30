import argparse
import time
import boto3
from sources.sftp_source import get_sftp_file
from upload.s3_upload import multipart_upload
from upload.validation import compare_sha256_with_s3

# Placeholder imports for future flows
# from sources.oracle_source import stream_oracle_to_file
# from sources.postgres_source import stream_postgres_to_file
# from sources.snowflake_source import stream_snowflake_to_file

def sftp_to_s3(args):
    """
    Flow: SFTP file → S3
    """
    timestamp = int(time.time())
    s3_key = f"{args.s3_key}_{timestamp}" if args.s3_key else f"{args.file_name}_{timestamp}"

    # Stream file from SFTP
    remote_file, sftp, ssh = get_sftp_file(
        ssh_host=args.ssh_host,
        ssh_user=args.ssh_user,
        ssh_password=args.ssh_password,
        remote_path=args.file_name
    )

    try:
        # Upload file to S3
        local_sha256 = multipart_upload(remote_file, args.s3_client, bucket=args.s3_bucket, key=s3_key)
        # Validate uploaded file
        compare_sha256_with_s3(local_sha256, args.s3_client, bucket=args.s3_bucket, key=s3_key)
    finally:
        remote_file.close()
        sftp.close()
        ssh.close()


def main():
    parser = argparse.ArgumentParser(description="Data ingestion flows into S3")
    parser.add_argument("--flow", required=True, choices=["sftp_to_s3", "oracle_to_s3", "postgres_to_s3", "snowflake_to_s3"], help="Flow to execute")
    parser.add_argument("--file_name", help="Name of the file to process or source")
    parser.add_argument("--s3_bucket", default="raw", help="S3 bucket name")
    parser.add_argument("--s3_key", help="S3 key prefix / filename")
    parser.add_argument("--aws_access_key_id", default="test", help="AWS access key")
    parser.add_argument("--aws_secret_access_key", default="test", help="AWS secret key")
    parser.add_argument("--aws_endpoint_url", default="http://localhost:4566", help="AWS endpoint URL (Localstack or AWS)")
    parser.add_argument("--ssh_host", help="SFTP host")
    parser.add_argument("--ssh_user", help="SFTP username")
    parser.add_argument("--ssh_password", help="SFTP password")
    # Add DB connection args for future flows
    parser.add_argument("--db_conn_str", help="Database connection string")

    args = parser.parse_args()

    # Initialize S3 client
    args.s3_client = boto3.client(
        "s3",
        endpoint_url=args.aws_endpoint_url,
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        region_name="us-east-1"
    )

    # Trigger flow
    if args.flow == "sftp_to_s3":
        sftp_to_s3(args)
    elif args.flow == "oracle_to_s3":
        print("Oracle to S3 flow not implemented yet.")
    elif args.flow == "postgres_to_s3":
        print("Postgres to S3 flow not implemented yet.")
    elif args.flow == "snowflake_to_s3":
        print("Snowflake to S3 flow not implemented yet.")


if __name__ == "__main__":
    main()