import os
import uuid
from dotenv import load_dotenv
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.llms.ollama import Ollama
import boto3
from llama_index.core.storage.chat_store import SimpleChatStore

# 1. Load environment variables
load_dotenv()

# 2. Establish connection to DynamoDB
dynamodb_client = boto3.resource('dynamodb',
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
dynamodb_chat_store = SimpleChatStore(
    dynamodb_client=dynamodb_client,
    table_name="chat_history"
)

# 3. Initialize LLM
llm = Ollama(model="gemma3n")

# 4. Generate unique chat session key
chat_store_key = f"session_{uuid.uuid4()}"

# 5. Create chat memory buffer
memory = ChatMemoryBuffer.from_defaults(
    chat_store=dynamodb_chat_store,
    chat_store_key=chat_store_key,
    token_limit=3000
)

# 6. Create chat engine
chat_engine = SimpleChatEngine.from_defaults(
    llm=llm,
    memory=memory,
    system_prompt="You are a knowledgeable assistant who answers based on your own information. The conversation is stored in DynamoDB."
)

# 7. Interactive chat loop
print(f"Chat engine is ready! (Session key: {chat_store_key})")
print("Press Ctrl+C to exit\n")

while True:
    try:
        user_input = input("User: ")
        response = chat_engine.chat(user_input)
        print(f"Assistant: {response}")
    except KeyboardInterrupt:
        print("\nChat session terminated.")
        break