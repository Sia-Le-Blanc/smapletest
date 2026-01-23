# router.py
import requests

class Router:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model_id = "gemma2:9b"
        self.max_rounds = 5
    
    def decide(self, query, context=""):
        prompt = f"""당신은 기업의 비서실장입니다. 한국어로 답변하세요.

[질문] {query}
[이전 분석] {context if context else "없음"}

[임무] 이 문제 해결에 필요한 부서를 선택하세요.
- finance: 재무/회계/투자 관련
- hr: 인사/조직/노무 관련  
- legal: 법무/컴플라이언스/소송 관련

[출력 규칙]
필요한 부서명만 쉼표로 구분 (예: finance,hr)
설명 없이 부서명만 출력하세요."""

        data = {"model": self.model_id, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.url, json=data)
            result = response.json()['response'].strip().lower()
            departments = [d.strip() for d in result.split(',') if d.strip() in ['finance', 'hr', 'legal']]
            return departments if departments else ['finance', 'hr', 'legal']
        except:
            return ['finance', 'hr', 'legal']

    def should_continue(self, context, current_round):
        if current_round >= self.max_rounds:
            return False
            
        prompt = f"""당신은 기업 전략 총괄 임원입니다.

[현재 분석 결과]
{context}

[검토 항목]
1. 부서 간 의견 충돌이 있습니까? 
   (예: 재무는 비용절감 주장, 인사는 인력충원 주장)
   
2. 구체적 실행 방안이 제시되었습니까?
   (예: "검토 필요" 같은 모호한 표현만 있으면 안됨)
   
3. 새로운 연쇄 리스크가 발견되었습니까?
   (예: A부서 이슈가 B부서에 미칠 영향을 새로 발견)

[판단 기준]
- 위 3가지 중 하나라도 해당되면 -> "계속"
- 모두 해결되었으면 -> "완료"

결과 (완료/계속 중 한 단어만):"""

        data = {"model": self.model_id, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.url, json=data)
            result = response.json()['response'].strip()
            return "계속" in result
        except:
            return False