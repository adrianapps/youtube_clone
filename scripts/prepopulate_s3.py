import boto3
import os
from youtube_clone.settings import AWS_STORAGE_BUCKET_NAME, AWS_S3_ENDPOINT_URL


def upload_default_files():
    s3 = boto3.client('s3', endpoint_url=AWS_S3_ENDPOINT_URL)

    files = {
        'media/thumbnails/default_thumbnail.jpg': '/app/media/thumbnails/default_thumbnail.jpg',
        'media/avatars/default_avatar.jpg': '/app/media/avatars/default_avatar.jpg',
    }

    for key, file_path in files.items():
        abs_path = os.path.abspath(file_path)
        if os.path.exists(abs_path):
            with open(abs_path, 'rb') as file:
                s3.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, key)
            print(f"Uploaded {abs_path} to {key}")
        else:
            print(f"File {abs_path} does not exist")


if __name__ == '__main__':
    upload_default_files()
