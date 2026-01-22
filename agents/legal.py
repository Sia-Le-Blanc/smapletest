from google import genai
import os
import json

class LegalAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model_id = "gemini-1.5-flash"
        
        with open('data/legal_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def analyze(self, query, context=""):
        data_text = '\n'.join([f"{k}: {v}" for k, v in self.data.items()])
        
        prompt = f"""당신은 법무팀장입니다.

보유 데이터:
{data_text}

이전 맥락: {context}

질문: {query}

법무 데이터를 기반으로 핵심 리스크와 대책을 3줄 이내로 답변하세요."""

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        
        return response.text