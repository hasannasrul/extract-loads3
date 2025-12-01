import hashlib
import tempfile

def compare_sha256_with_s3(local_sha256, s3_client, bucket, key):
    """
    Downloads the uploaded file from S3 and compares SHA256 checksum.
    """
    with tempfile.NamedTemporaryFile() as tmpfile:
        s3_client.download_file(bucket, key, tmpfile.name)
        with open(tmpfile.name, "rb") as f:
            uploaded_sha256 = hashlib.sha256(f.read()).hexdigest()

    if local_sha256 == uploaded_sha256:
        print("✅ SHA256 validation passed: uploaded file matches original.")
        return True
    else:
        print("⚠️ SHA256 validation failed: uploaded file may be corrupted.")
        return False
