import requests
import json

class FinanceAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:2b"
        with open('data/finance_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def analyze(self, query, context=""):
        data_text = json.dumps(self.data, ensure_ascii=False)
        prompt = f"""당신은 CFO입니다. 한국어로 답변하세요.
[나의 재무 데이터] {data_text}
[타 부서 분석 맥락] {context}
[질문] {query}

[지침]
1. 재무 지표를 분석하되, [타 부서 맥락]에 있는 이슈(이직률, 소송 등)가 재무적 손실에 미칠 연쇄 영향을 분석하세요.
2. 답변은 '핵심 지표', '부서 간 연계 리스크', '대응 방향'으로 구성하세요."""
        
        data = {"model": self.model_id, "prompt": prompt, "stream": False}
        return requests.post(self.url, json=data).json()['response']