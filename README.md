# Extract and Load to S3

### This is a repo to read data from different data source and place original file to s3

Sample script to run this repo
'''
python main.py \
    --flow sftp_to_s3 \
    --file_name "/Users/hasan/Nasrul/Learning/Python/Data Engineering/Dataset/people-2000000.zip" \
    --s3_bucket raw \
    --ssh_host 192.168.1.15 \
    --ssh_user xxxx \
    --ssh_password xxxx
'''