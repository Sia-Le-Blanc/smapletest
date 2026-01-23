import requests
import json

class Router:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        # 더 정교한 판단을 위해 9b 모델 적용
        self.model_id = "gemma2:9b" 
    
    def decide(self, query, context=""):
        prompt = f"""당신은 기업의 비서실장입니다. 한국어로 답변하세요.
[상황] {query}
[이전 분석 맥락] {context if context else "없음"}

[임무] 이 문제를 해결하기 위해 어떤 부서의 전문 분석이 필요한지 결정하세요.
선택 가능 부서: finance(재무), hr(인사), legal(법무)

[응답 규칙]
- 필요한 부서 이름만 쉼표로 구분하여 출력 (예: finance,hr)
- 설명 없이 부서명만 정확히 출력하세요."""

        data = {"model": self.model_id, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.url, json=data)
            result = response.json()['response']
            return [a.strip().lower() for a in result.split(',') if a.strip()]
        except Exception as e:
            return ['finance', 'hr', 'legal']

    def should_continue(self, context):
        prompt = f"""당신은 기업 비서실장입니다. 
[현재 분석 결과]
{context}

[판단 기준]
- 각 부서가 자기 부서 데이터만 나열하고 있는가? -> "계속" (합동 토론 필요)
- 부서 간의 연쇄 리스크(예: 재무 위기가 인사 이탈에 미치는 영향 등)가 충분히 분석되었는가? -> "완료"

결과(완료 또는 계속 중 한 단어만):"""
        data = {"model": self.model_id, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.url, json=data)
            return "계속" in response.json()['response']
        except:
            return False