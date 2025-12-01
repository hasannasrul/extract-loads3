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

| Argument                  | Required          | Description                              |
| ------------------------- | ----------------- | ---------------------------------------- |
| `--flow`                  | Yes               | Which flow to run (`sftp_to_s3`, etc.)   |
| `--file_name`             | Yes               | Remote or local file path                |
| `--s3_bucket`             | Yes               | Destination S3 bucket                    |
| `--s3_key`                | No                | Custom S3 key prefix                     |
| `--ssh_host`              | Required for SFTP | SFTP server address                      |
| `--ssh_user`              | Required for SFTP | SFTP username                            |
| `--ssh_password`          | Required for SFTP | SFTP password                            |
| `--aws_access_key_id`     | No                | AWS key (default: `test` for Localstack) |
| `--aws_secret_access_key` | No                | AWS secret (default: `test`)             |
| `--aws_endpoint_url`      | No                | AWS endpoint or Localstack               |


## 1. SFTP → S3

This flow:

Connects to an SFTP server

Streams the remote file

Uploads the file to S3 using multipart upload

Validates file integrity via SHA256 checksum

```bash
--flow sftp_to_s3
```

