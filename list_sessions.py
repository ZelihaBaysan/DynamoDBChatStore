import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb',
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
table = dynamodb.Table("chat_history")

# Scan the table for all session keys
response = table.scan(
    ProjectionExpression="session_id"
)

# Extract session keys
session_keys = [item['session_id'] for item in response.get('Items', [])]

if not session_keys:
    print("No sessions found in DynamoDB.")
else:
    print(f"{len(session_keys)} session(s) found:\n")
    for key in session_keys:
        print(f"- {key}")