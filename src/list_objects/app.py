import json
import boto3
from botocore.exceptions import ClientError


s3 = boto3.client("s3")


def response(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters") or {}
        bucket_name = query_params.get("bucket")

        if not bucket_name:
            return response(400, {
                "error": "Missing required query parameter: bucket"
            })

        s3_response = s3.list_objects_v2(Bucket=bucket_name)

        objects = [
            {
                "key": item["Key"],
                "size": item["Size"],
                "last_modified": item["LastModified"].isoformat()
            }
            for item in s3_response.get("Contents", [])
        ]

        return response(200, {
            "bucket": bucket_name,
            "objects": objects
        })

    except ClientError as error:
        error_code = error.response.get("Error", {}).get("Code", "Unknown")

        if error_code == "NoSuchBucket":
            return response(404, {
                "error": "Bucket does not exist",
                "bucket": bucket_name
            })

        if error_code == "AccessDenied":
            return response(403, {
                "error": "Access denied to bucket",
                "bucket": bucket_name
            })

        return response(500, {
            "error": str(error)
        })

    except Exception as error:
        return response(500, {
            "error": str(error)
        })
