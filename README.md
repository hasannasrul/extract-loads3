# 📦 extract-loads3

A simple, extensible Python utility to **extract data from different sources and load the original files into Amazon S3** It can be used in different data pipeline orchestration tool like airflow.

**Pypi repo link**
```
https://pypi.org/project/extract-loads3/
```
Currently supported:

- **SFTP → S3** (fully functional)

More data sources (Postgres, Oracle, Snowflake, etc.) will be added soon.

---

## 🚀 Installation

```bash
pip install extract-loads3
```

once installed run

```bash
extract-loads3 \
    --flow sftp_to_s3 \
    --file_name "/path/to/file.zip" \
    --s3_bucket raw \
    --ssh_host 192.168.1.15 \
    --ssh_user your_username \
    --ssh_password your_password
```

You do not need to pass AWS credentials or endpoint URL unless:
you want to override environment/IAM role credentials
you’re using LocalStack or MinIO

| Argument                  | Required?         | Description                                                  |
| ------------------------- | ----------------- | ------------------------------------------------------------ |
| `--flow`                  | **Yes**           | Which ingestion flow to run (`sftp_to_s3`, more coming soon) |
| `--file_name`             | **Yes** for SFTP  | Remote SFTP file path                                        |
| `--s3_bucket`             | **Yes**           | Destination S3 bucket                                        |
| `--s3_key`                | No                | Custom S3 key / prefix; if omitted, timestamp is appended    |
| `--ssh_host`              | Required for SFTP | SFTP server host                                             |
| `--ssh_user`              | Required for SFTP | SFTP username                                                |
| `--ssh_password`          | Required for SFTP | SFTP password                                                |
| `--aws_access_key_id`     | No                | AWS key; if omitted, boto3 uses IAM role / env vars          |
| `--aws_secret_access_key` | No                | AWS secret                                                   |
| `--aws_endpoint_url`      | No                | Custom S3 endpoint (LocalStack, MinIO, custom S3 gateways)   |
| `--db_conn_str`           | No                | Future DB connection string                                  |



## 1. SFTP → S3

This flow:

Connects to an SFTP server <br>
Streams the remote file <br>
Uploads the file to S3 using multipart upload <br>
Validates file integrity via SHA256 checksum <br>

```bash
--flow sftp_to_s3
```

to use with localstacl
```
--aws_endpoint_url http://localhost:4566 \
--aws_access_key_id test \
--aws_secret_access_key test

```