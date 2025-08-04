import os
import uuid
import boto3
from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

# Ortam değişkenlerini yükle
load_dotenv()

# DynamoDB bağlantısı oluştur
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
table = dynamodb.Table("chat_history")

# LLM başlat
llm = Ollama(model="gemma3n")

# Benzersiz session ID üret
session_id = f"session_{uuid.uuid4()}"
print(f"Chat engine is ready! (Session key: {session_id})")
print("Press Ctrl+C to exit\n")

# Chat geçmişini tutan liste
chat_history = []

# Chat döngüsü
while True:
    try:
        user_input = input("User: ")
        chat_history.append(f"User: {user_input}")

        # ChatMessage nesnesi oluştur
        message = ChatMessage(role="user", content=user_input)
        
        # Düzeltilmiş kısım: ChatMessage nesnesi kullanılıyor
        response = llm.chat(messages=[message])
        assistant_reply = response.message.content

        print(f"Assistant: {assistant_reply}")
        chat_history.append(f"Assistant: {assistant_reply}")

        # Her mesajdan sonra DynamoDB'ye kaydet
        table.put_item(
            Item={
                'session_id': session_id,
                'history': chat_history
            }
        )

    except KeyboardInterrupt:
        print("\nChat session terminated.")
        break