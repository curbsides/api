import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from botocore.exceptions import NoCredentialsError, ClientError
import boto3
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_REGION = os.getenv("S3_REGION")

router = APIRouter()

s3_client = boto3.client(
    "s3",
    region_name=S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

@router.get("/{filename}")
async def serve_image(filename: str):
    try:
        s3_object = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=f'images/{filename}')
        file_stream = s3_object["Body"]
        
        return StreamingResponse(
            file_stream,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="AWS credentials not found")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(status_code=404, detail="File not found in S3")
        else:
            raise HTTPException(status_code=500, detail="Error fetching file from S3")