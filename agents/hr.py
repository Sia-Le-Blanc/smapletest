# agents/hr.py
import requests
import json

class HRAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:2b"
        with open('data/hr_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def analyze(self, query, context=""):
        data_text = json.dumps(self.data, ensure_ascii=False, indent=2)
        prompt = f"""당신은 CHRO(최고인사책임자)입니다. 한국어로 답변하세요.

[인사 데이터]
{data_text}

[타 부서 분석 결과]
{context if context else "아직 다른 부서 분석이 없습니다."}

[질문]
{query}

[분석 지침]
1. 인사 현황을 객관적으로 분석하세요
2. 재무 위기나 법적 이슈가 조직에 미칠 심리적/조직적 영향을 분석하세요
3. 타 부서 제안과 충돌되는 부분이 있다면 명확히 지적하세요

[출력 형식]
## 인사 현황 진단
- 핵심 지표 분석 (이직률, 만족도 등)
- 위험 수준 (상/중/하)

## 타 부서 연계 리스크
- 재무팀 이슈의 인사 영향 (예: 구조조정 → 핵심인력 유출)
- 법무팀 이슈의 인사 영향 (예: 노동분쟁 → 조직 사기 저하)

## 인사 차원 대응 방안
- 구체적 실행 액션 (예: 핵심인력 X명 리텐션 프로그램)
- 타 부서 협조 필요 사항

답변:"""
        
        data = {"model": self.model_id, "prompt": prompt, "stream": False}
        return requests.post(self.url, json=data).json()['response']