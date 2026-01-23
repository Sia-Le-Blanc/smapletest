import requests
import json

class Router:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:2b"
    
    def decide(self, query, context=""):
        prompt = f"""당신은 기업 비서실장입니다. 한국어로만 답변하세요.

[이전 분석 맥락]
{context}

[현재 질문]
{query}

[임무]
이 질문을 해결하기 위해 어떤 전문가의 분석이 필요한지 판단하세요.

선택 가능한 전문가:
- finance: 재무/회계/자금 관련
- hr: 인사/조직/인력 관련  
- legal: 법무/소송/컴플라이언스 관련

[응답 규칙]
- 필요한 전문가 이름만 쉼표로 구분하여 작성
- 예시: finance,hr
- 설명 없이 전문가 이름만 출력"""

        data = {
            "model": self.model_id,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(self.url, json=data)
        result = response.json()['response']
        agents = result.strip().lower().replace(' ', '').split(',')
        return agents
    
    def should_continue(self, context):
        prompt = f"""당신은 기업 비서실장입니다. 한국어로만 답변하세요.

[분석 결과]
{context}

[판단 기준]
현재 분석 결과만으로 경영진이 의사결정을 내릴 수 있는가?

- 각 부서의 문제점이 명확하게 파악되었다 → "완료"
- 분석이 너무 피상적이거나 애매하다 → "계속"
- 이미 충분히 상세한 분석이 완료되었다면, 추가 분석은 불필요 → "완료"

중요: 모든 부서를 반드시 분석할 필요는 없음. 현재 분석된 부서들의 내용이 충분하면 완료.

결과: (완료 또는 계속 중 한 단어만)"""

        data = {
            "model": self.model_id,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(self.url, json=data)
        result = response.json()['response']
        return "계속" in result