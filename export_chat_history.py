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

chat_store_key = input("Enter the session key you want to retrieve (e.g., session_1): ")

# Query the table for the specific session
response = table.get_item(
    Key={
        'session_id': chat_store_key
    }
)

if 'Item' not in response:
    print(f"No records found for session key: {chat_store_key}")
else:
    chat_history = response['Item'].get('history', [])
    with open("dynamodb_chat_history.txt", "w", encoding="utf-8") as f:
        f.write(f"CHAT HISTORY ({chat_store_key})\n")
        f.write("-" * 50 + "\n")
        for msg in chat_history:
            f.write(msg + "\n")
    print("Chat history has been written to 'dynamodb_chat_history.txt'.")