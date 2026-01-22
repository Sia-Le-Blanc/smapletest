import requests
import json
import os

class FinanceAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:2b"
        
        with open('data/finance_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def analyze(self, query, context=""):
        data_text = '\n'.join([f"{k}: {v}" for k, v in self.data.items()])
        
        prompt = f"""당신은 CFO입니다. 한국어로만 답변하세요.

[재무 데이터]
{data_text}

[이전 맥락]
{context}

[질문]
{query}

[답변 규칙]
- 핵심만 5줄 이내로 요약
- 구체적 수치 포함
- 실행 가능한 방안 제시"""

        data = {
            "model": self.model_id,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(self.url, json=data)
        return response.json()['response']