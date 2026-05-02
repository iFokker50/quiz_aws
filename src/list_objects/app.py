import json
import boto3


s3 = boto3.client("s3")


def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters") or {}
        bucket_name = query_params.get("bucket")

        if not bucket_name:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "Missing required query parameter: bucket"
                })
            }

        response = s3.list_objects_v2(Bucket=bucket_name)

        objects = [
            {
                "key": item["Key"],
                "size": item["Size"],
                "last_modified": item["LastModified"].isoformat()
            }
            for item in response.get("Contents", [])
        ]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "bucket": bucket_name,
                "objects": objects
            })
        }

    except Exception as error:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(error)
            })
        }