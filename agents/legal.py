import requests
import json
import os

class LegalAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:2b"
        
        with open('data/legal_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def analyze(self, query, context=""):
        data_text = '\n'.join([f"{k}: {v}" for k, v in self.data.items()])
        
        prompt = f"""당신은 법무팀장입니다. 한국어로만 답변하세요.

[법무 데이터]
{data_text}

[이전 맥락]
{context}

[질문]
{query}

[답변 예시]
1. 진행 중인 소송 7건, 총 소송금액 230억원으로 재무 리스크 심각
2. 특허침해 소송 1심 패소로 손해배상 85억원 확정, 항소 준비 중
3. 대표이사 횡령 내부고발 건 검찰 이첩 예정, 기업 이미지 타격 우려

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