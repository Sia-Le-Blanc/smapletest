# agents/legal.py
import requests
import json

class LegalAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:2b"
        with open('data/legal_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def analyze(self, query, context=""):
        data_text = json.dumps(self.data, ensure_ascii=False, indent=2)
        prompt = f"""당신은 CLO(최고법무책임자)입니다. 한국어로 답변하세요.

[법무 데이터]
{data_text}

[타 부서 분석 결과]
{context if context else "아직 다른 부서 분석이 없습니다."}

[질문]
{query}

[분석 지침]
1. 법적 리스크를 객관적으로 분석하세요
2. 재무 위기나 인사 이슈가 법적 분쟁으로 번질 가능성을 분석하세요
3. 타 부서 제안과 충돌되는 부분이 있다면 명확히 지적하세요

[출력 형식]
## 법무 리스크 진단
- 핵심 법적 이슈 분석 (소송, 컴플라이언스 등)
- 위험 수준 (상/중/하)

## 타 부서 연계 리스크
- 재무팀 이슈의 법무 영향 (예: 계약 해지 → 손해배상 소송)
- 인사팀 이슈의 법무 영향 (예: 임금협상 결렬 → 노동청 진정)

## 법무 차원 대응 방안
- 구체적 실행 액션 (예: 소송 X건 합의 추진, 컴플라이언스 점검)
- 타 부서 협조 필요 사항

답변:"""
        
        data = {"model": self.model_id, "prompt": prompt, "stream": False}
        return requests.post(self.url, json=data).json()['response']