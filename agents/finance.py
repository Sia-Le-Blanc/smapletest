# agents/finance.py
import requests
import json

class FinanceAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:2b"
        with open('data/finance_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def analyze(self, query, context=""):
        data_text = json.dumps(self.data, ensure_ascii=False, indent=2)
        prompt = f"""당신은 CFO(최고재무책임자)입니다. 한국어로 답변하세요.

[재무 데이터]
{data_text}

[타 부서 분석 결과]
{context if context else "아직 다른 부서 분석이 없습니다."}

[질문]
{query}

[분석 지침]
1. 재무 지표를 객관적으로 분석하세요
2. 타 부서 이슈(이직률, 소송 등)가 재무에 미칠 구체적 영향을 금액으로 추정하세요
3. 타 부서 제안과 충돌되는 부분이 있다면 명확히 지적하세요

[출력 형식]
## 재무 진단
- 핵심 지표 분석
- 위험 수준 (상/중/하)

## 타 부서 연계 리스크
- 인사팀 이슈의 재무 영향 (예: 이직률 상승 → 채용비 증가)
- 법무팀 이슈의 재무 영향 (예: 소송 → 손해배상)

## 재무 차원 대응 방안
- 구체적 실행 액션 (예: 예산 X억 확보, 계약 Y건 재협상)
- 타 부서 협조 필요 사항

답변:"""
        
        data = {"model": self.model_id, "prompt": prompt, "stream": False}
        return requests.post(self.url, json=data).json()['response']