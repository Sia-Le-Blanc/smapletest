import requests
import json
import os

class HRAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:2b"
        
        with open('data/hr_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def analyze(self, query, context=""):
        data_text = '\n'.join([f"{k}: {v}" for k, v in self.data.items()])
        
        prompt = f"""당신은 인사팀장입니다. 한국어로만 답변하세요.

[인사 데이터]
{data_text}

[이전 맥락]
{context}

[질문]
{query}

[답변 예시]
1. 이직률 18.3%로 전년대비 7.2%p 급증, 핵심인력 23명 퇴사로 조직 불안정
2. 직원만족도 52점으로 전년 73점 대비 21점 하락, 근속연수 4.2년으로 감소 추세
3. 월평균 초과근무 68시간으로 법정한도 초과, 노조 임금협상 결렬 상태

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