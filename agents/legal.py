import requests
import json

class LegalAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:2b"
        with open('data/legal_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def analyze(self, query, context=""):
        data_text = json.dumps(self.data, ensure_ascii=False)
        prompt = f"""당신은 법무팀장입니다. 한국어로 답변하세요.

[나의 법무 데이터]
{data_text}

[타 부서 분석 및 이전 맥락]
{context if context else "아직 타 부서의 분석이 없습니다."}

[질문]
{query}

[분석 지침]
1. 법적 리스크를 분석하되, 특히 인사팀의 임금 협상 결렬이나 재무팀의 계약 해지 이슈가 실제 소송이나 과징금으로 번질 가능성을 집중 검토하세요.
2. 타 부서 이슈와 연계된 '법적 도미노 리스크'를 찾아내세요.
3. 답변은 '법무 리스크 진단', '부서 협력 필요 사항', '법적 대응 전략'의 3항목으로 작성하세요."""
        
        data = {"model": self.model_id, "prompt": prompt, "stream": False}
        response = requests.post(self.url, json=data)
        return response.json()['response']