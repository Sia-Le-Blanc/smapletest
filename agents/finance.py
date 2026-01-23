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

[답변 예시]
1. 매출 850억원으로 전년대비 28.3% 급감, 주요 고객사 2곳 계약 해지가 직접적 원인
2. 영업이익 -50억원 적자 전환, 원자재 가격 상승으로 원가율 12%p 증가
3. 부채비율 68.2%로 안정권 초과, 긴급 구조조정 필요

[답변 규칙]
- 위 예시처럼 문제점만 1, 2, 3 형식으로 나열
- 각 항목은 한 줄로 작성
- 구체적 수치 반드시 포함
- 해결방안 제시하지 말 것"""

        data = {
            "model": self.model_id,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(self.url, json=data)
        return response.json()['response']