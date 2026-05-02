import json
import boto3


s3 = boto3.client("s3")


def lambda_handler(event, context):
    try:
        response = s3.list_buckets()

        buckets = [
            {
                "name": bucket["Name"],
                "creation_date": bucket["CreationDate"].isoformat()
            }
            for bucket in response.get("Buckets", [])
        ]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "buckets": buckets
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