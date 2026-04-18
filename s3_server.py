import os
import boto3
from mcp.server.fastmcp import FastMCP
from botocore.exceptions import ClientError

# Initialize FastMCP server
mcp = FastMCP("s3-server")

def get_s3_client():
    """
    Returns a boto3 S3 client.
    Assumes credentials are provided via environment variables,
    AWS config file, or IAM role.
    """
    return boto3.client('s3')

@mcp.tool()
def list_s3_files(bucket_name: str, prefix: str = "") -> str:
    """
    Lists files in an S3 bucket, optionally filtered by a prefix.

    Args:
        bucket_name: The name of the S3 bucket.
        prefix: Optional prefix to filter the files (e.g., "photos/").
    """
    try:
        s3 = get_s3_client()
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if 'Contents' not in response:
            return f"No files found in bucket '{bucket_name}' with prefix '{prefix}'."

        files = [obj['Key'] for obj in response['Contents']]
        return "\n".join(files)
    except ClientError as e:
        return f"S3 Client Error: {str(e)}"
    except Exception as e:
        return f"Error listing S3 files: {str(e)}"

@mcp.tool()
def download_s3_file(bucket_name: str, file_key: str, destination_path: str) -> str:
    """
    Downloads a file from an S3 bucket to a local path.

    Args:
        bucket_name: The name of the S3 bucket.
        file_key: The key (path) of the file in the bucket.
        destination_path: The local absolute path where the file should be saved.
    """
    try:
        s3 = get_s3_client()
        s3.download_file(bucket_name, file_key, destination_path)
        return f"Successfully downloaded s3://{bucket_name}/{file_key} to {destination_path}"
    except ClientError as e:
        return f"S3 Client Error: {str(e)}"
    except Exception as e:
        return f"Error downloading S3 file: {str(e)}"

if __name__ == "__main__":
    mcp.run()
