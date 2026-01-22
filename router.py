from google import genai
import os

class Router:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model_id = "gemini-1.5-flash"
    
    def decide(self, query, context=""):
        prompt = f"""당신은 비서실장입니다. 질문을 분석하여 어떤 전문가에게 맡길지 결정하세요.

이전 맥락: {context}

질문: {query}

선택 가능한 전문가: finance, hr, legal
여러 명이 필요하면 쉼표로 구분 (예: finance,hr)

답변 형식: 전문가이름만 (설명 없이)"""

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        
        agents = response.text.strip().lower().replace(' ', '').split(',')
        return agents
    
    def should_continue(self, context):
        prompt = f"""당신은 비서실장입니다. 지금까지의 분석 결과를 보고 추가 분석이 필요한지 판단하세요.

분석 결과:
{context}

충분한 인사이트를 얻었으면 "완료", 더 필요하면 "계속"이라고만 답하세요."""

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        
        return "계속" in response.text