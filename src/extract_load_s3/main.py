import argparse
import time
import boto3

from extract_load_s3.sources.sftp_source import get_sftp_file
from extract_load_s3.upload.s3_upload import multipart_upload
from extract_load_s3.upload.validation import compare_sha256_with_s3


# -------------------------
# FLOW: SFTP → S3
# -------------------------
def sftp_to_s3(args):
    timestamp = int(time.time())
    s3_key = f"{args.s3_key}_{timestamp}" if args.s3_key else f"{args.file_name}_{timestamp}"

    # Pull file from SFTP
    remote_file, sftp, ssh = get_sftp_file(
        ssh_host=args.ssh_host,
        ssh_user=args.ssh_user,
        ssh_password=args.ssh_password,
        remote_path=args.file_name
    )

    try:
        # Upload to S3
        local_sha256 = multipart_upload(
            remote_file,
            args.s3_client,
            bucket=args.s3_bucket,
            key=s3_key
        )
        # Validate upload
        compare_sha256_with_s3(local_sha256, args.s3_client, bucket=args.s3_bucket, key=s3_key)
    finally:
        remote_file.close()
        sftp.close()
        ssh.close()


# -------------------------
# MAIN ENTRYPOINT
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Unified Data Ingestion into S3")

    parser.add_argument(
        "--flow",
        required=True,
        choices=["sftp_to_s3", "oracle_to_s3", "postgres_to_s3", "snowflake_to_s3"],
        help="Ingestion flow to execute"
    )

    # General arguments
    parser.add_argument("--file_name", help="Remote filename or source identifier", required=False)
    parser.add_argument("--s3_bucket", default="raw", help="Target S3 bucket")
    parser.add_argument("--s3_key", help="Target S3 key prefix (optional)")

    # Optional AWS settings
    parser.add_argument("--aws_access_key_id", help="AWS Access Key", required=False)
    parser.add_argument("--aws_secret_access_key", help="AWS Secret Key", required=False)
    parser.add_argument("--aws_endpoint_url", help="Custom S3 endpoint (LocalStack, MinIO, etc.)", required=False)

    # SFTP args
    parser.add_argument("--ssh_host", help="SFTP host")
    parser.add_argument("--ssh_user", help="SFTP username")
    parser.add_argument("--ssh_password", help="SFTP password")

    # Placeholder for DB flows
    parser.add_argument("--db_conn_str", help="DB connection string for supported DB flows")

    args = parser.parse_args()

    # -------------------------
    # Create Boto3 S3 Client
    # -------------------------
    s3_kwargs = {
        "region_name": "us-east-1"
    }

    # Only use credentials if user explicitly provides them
    if args.aws_access_key_id and args.aws_secret_access_key:
        s3_kwargs["aws_access_key_id"] = args.aws_access_key_id
        s3_kwargs["aws_secret_access_key"] = args.aws_secret_access_key

    # Only add endpoint URL if provided
    if args.aws_endpoint_url:
        s3_kwargs["endpoint_url"] = args.aws_endpoint_url

    args.s3_client = boto3.client("s3", **s3_kwargs)

    # -------------------------
    # Pick flow
    # -------------------------
    if args.flow == "sftp_to_s3":
        sftp_to_s3(args)
    elif args.flow == "oracle_to_s3":
        print("Oracle → S3 flow not implemented yet.")
    elif args.flow == "postgres_to_s3":
        print("Postgres → S3 flow not implemented yet.")
    elif args.flow == "snowflake_to_s3":
        print("Snowflake → S3 flow not implemented yet.")
    else:
        raise ValueError("Unknown flow")


if __name__ == "__main__":
    main()
