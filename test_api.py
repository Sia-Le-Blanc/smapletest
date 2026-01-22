from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="안녕하세요, 간단히 답변해주세요."
)

print(response.text)