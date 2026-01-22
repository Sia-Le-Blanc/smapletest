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

[지금까지의 분석 결과]
{context}

[임무]
위 분석 결과가 경영진에게 보고하기에 충분한지 판단하세요.

판단 기준:
- 문제의 원인이 명확히 파악되었는가?
- 구체적인 해결 방안이 제시되었는가?
- 추가 분석이 필요한 영역이 있는가?

[응답 규칙]
충분하면: "완료"
부족하면: "계속"
(설명 없이 한 단어만 출력)"""

        data = {
            "model": self.model_id,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(self.url, json=data)
        result = response.json()['response']
        return "계속" in result