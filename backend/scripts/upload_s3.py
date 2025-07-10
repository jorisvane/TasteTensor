import boto3
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
bucket_name = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region,
)

def upload_file(local_path: str, s3_key: str):
    with open(local_path, "rb") as f:
        s3.upload_fileobj(f, bucket_name, s3_key)
    print(f"Uploaded file {local_path} to S3")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.abspath(os.path.join(script_dir, "..", "..", "data", "kaggle-recipes", "food-images"))

    print(image_dir)

    for file_name in os.listdir(image_dir):
        print(file_name)
        if file_name.lower().endswith(".jpg"):
            local_path = os.path.join(image_dir, file_name)
            s3_key = f"food-images/{file_name}"
            upload_file(local_path, s3_key)