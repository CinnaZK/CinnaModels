import os
import argparse
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Constants for environment variables
S3_ENDPOINT = os.getenv('S3_ENDPOINT')
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
REGION_NAME = 'enam'

# Initialize S3 client for Cloudflare R2
s3_client = boto3.client(
    's3',
    region_name=REGION_NAME,
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

def upload_file(file_path, bucket, filename):
    """Upload a single file to the specified bucket."""
    s3_client.upload_file(file_path, bucket, filename)
    print(f'Uploaded {file_path} to {bucket}/{filename}')

def upload_directory(directory_path, bucket):
    """Upload all files from a directory to the specified bucket."""
    for file in Path(directory_path).iterdir():
        if file.is_file():
            upload_file(str(file), bucket, file.name)

def main():
    parser = argparse.ArgumentParser(description="Upload files or directories to Cloudflare R2.")
    parser.add_argument('--dir', help='Directory containing files to upload')
    parser.add_argument('--file', help='Single file to upload')
    parser.add_argument('--bucket', required=True, help='Name of the Cloudflare R2 bucket')
    args = parser.parse_args()

    if args.file:
        file_path = Path(args.file)
        if file_path.is_file():
            upload_file(str(file_path), args.bucket, file_path.name)
        else:
            print(f'Error: {file_path} is not a valid file.')
    elif args.dir:
        dir_path = Path(args.dir)
        if dir_path.is_dir():
            upload_directory(dir_path, args.bucket)
        else:
            print(f'Error: {dir_path} is not a valid directory.')
    else:
        print('Error: Provide either --file or --dir argument.')

if __name__ == "__main__":
    main()
