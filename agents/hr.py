import requests
import json

class HRAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:2b"
        with open('data/hr_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def analyze(self, query, context=""):
        data_text = json.dumps(self.data, ensure_ascii=False)
        prompt = f"""당신은 인사팀장입니다. 한국어로 답변하세요.
[나의 인사 데이터] {data_text}
[타 부서 분석 맥락] {context}
[질문] {query}

[지침]
1. 인사 현황을 분석하되, 재무적 위기나 구조조정 계획이 직원 사기 및 인력 유출에 미칠 심리적/조직적 영향을 분석하세요.
2. 답변은 '인사 현황', '조직 연쇄 리스크', '인사 차원 대응'으로 구성하세요."""
        
        data = {"model": self.model_id, "prompt": prompt, "stream": False}
        return requests.post(self.url, json=data).json()['response']