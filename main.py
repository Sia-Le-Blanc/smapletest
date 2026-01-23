import os
import asyncio
from dotenv import load_dotenv
from router import Router
from agents import FinanceAgent, HRAgent, LegalAgent
from memory.shared_memory import SharedMemory
import requests

load_dotenv()

def run_agent(agent, name, query, context):
    print(f"  → {name} 분석 시작...")
    result = agent.analyze(query, context)
    print(f"  ✓ {name} 완료")
    return name, result

def generate_final_solution(memory):
    print("\n" + "=" * 60)
    print("최종 전략 보고서 생성 중...")
    print("=" * 60)
    
    prompt = f"""당신은 CEO입니다. 한국어로만 답변하세요.

[각 부서 분석 결과]
{memory.get_context()}

[보고서 예시]
## 경영 위기 종합 진단

### 핵심 문제
1. 매출 급감 및 적자 전환으로 재무 위기 심화
2. 대규모 인력 이탈로 조직 경쟁력 약화
3. 법적 리스크 230억원으로 생존 위협

### 긴급 실행 과제
1. 주요 고객사 신뢰 회복 프로그램 (재무팀, 1개월)
2. 핵심인력 긴급 retention 패키지 (인사팀, 즉시)
3. 소송 리스크 최소화 전략 수립 (법무팀, 2주)

### 예상 효과
- 3개월 내 매출 15% 회복 가능
- 이직률 10%p 감소 예상
- 법적 리스크 30% 감축

[작성 규칙]
- 위 형식을 따를 것
- 각 부서 분석을 통합하여 작성
- 구체적 수치와 기간 명시"""

    data = {
        "model": "gemma2:2b",
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post("http://localhost:11434/api/generate", json=data)
    return response.json()['response']

def recursive_analysis(router, agents_map, memory, query, depth=0):
    print(f"\n{'  ' * depth}[Depth {depth+1}: Router Decision]")
    selected = router.decide(query, memory.get_context())
    print(f"{'  ' * depth}  선택된 전문가: {', '.join(selected)}")
    
    print(f"{'  ' * depth}[Depth {depth+1}: Agent Execution (순차)]")
    results = []
    for agent_name in selected:
        if agent_name in agents_map:
            name, result = run_agent(agents_map[agent_name], agent_name, query, memory.get_context())
            results.append((name, result))
    
    for name, result in results:
        print(f"\n{'  ' * depth}[{name.upper()} 분석 결과]")
        if result:
            print(result)
            memory.add(depth+1, name, result)
        else:
            print(f"{'  ' * depth}결과 없음")
    
    print(f"\n{'  ' * depth}[Router 종료 판단 중...]")
    if router.should_continue(memory.get_context()):
        print(f"{'  ' * depth}  → 추가 분석 필요")
        recursive_analysis(router, agents_map, memory, "이전 분석을 심화하여 최종 전략 도출", depth+1)
    else:
        print(f"{'  ' * depth}  → 분석 충분, 종료")

def main():
    print("=" * 60)
    print("Corporate Brain System (순차 실행)")
    print("=" * 60)
    
    router = Router()
    memory = SharedMemory()
    
    agents_map = {
        'finance': FinanceAgent(),
        'hr': HRAgent(),
        'legal': LegalAgent()
    }
    
    query = "회사원들의 불만이 많아졌습니다. 종합 분석이 필요합니다."
    
    print(f"\n[초기 질문] {query}")
    
    recursive_analysis(router, agents_map, memory, query)
    
    final_solution = generate_final_solution(memory)
    print("\n" + final_solution)
    
    print("\n" + "=" * 60)
    print("분석 완료")
    print("=" * 60)

if __name__ == "__main__":
    main()