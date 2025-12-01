import hashlib
from botocore.exceptions import ClientError

def multipart_upload(file_obj, s3_client, bucket, key, part_size=50*1024*1024, max_retries=3):
    """
    Uploads a file-like object to S3 using multipart upload.
    Returns the SHA256 checksum of the file content.
    """
    sha256 = hashlib.sha256()

    # Start multipart upload
    multipart = s3_client.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = multipart["UploadId"]
    parts = []
    part_number = 1

    try:
        while True:
            chunk = file_obj.read(part_size)
            if not chunk:
                break
            sha256.update(chunk)

            for attempt in range(1, max_retries+1):
                try:
                    part = s3_client.upload_part(
                        Bucket=bucket,
                        Key=key,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=chunk
                    )
                    parts.append({"ETag": part["ETag"], "PartNumber": part_number})
                    break
                except Exception as e:
                    print(f"Part {part_number} upload failed (attempt {attempt}): {e}")
                    if attempt == max_retries:
                        raise
                    print("Retrying...")

            part_number += 1

        s3_client.complete_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts}
        )
        print(f"Upload complete → s3://{bucket}/{key}")

        return sha256.hexdigest()

    except Exception as e:
        print("Error during upload, aborting multipart upload...")
        s3_client.abort_multipart_upload(Bucket=bucket, Key=key, UploadId=upload_id)
        raise e
    finally:
        file_obj.close()
