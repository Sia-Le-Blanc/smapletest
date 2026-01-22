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

[임무]
위 분석을 종합하여 이사회에 보고할 최종 전략을 작성하세요.

[보고서 형식]
## 경영 위기 종합 진단 보고서

### 1. 핵심 문제 요약
(재무/인사/법무 관점에서 발견된 주요 문제 통합 정리)

### 2. 긴급 실행 과제 (우선순위 Top 3)
1. [과제명] - 담당: [부서] / 기한: [기간] / 예상효과: [내용]
2. [과제명] - 담당: [부서] / 기한: [기간] / 예상효과: [내용]
3. [과제명] - 담당: [부서] / 기한: [기간] / 예상효과: [내용]

### 3. 중장기 개선 로드맵 (6개월)
- 3개월 이내: 
- 6개월 이내:

### 4. 예상 성과 및 리스크
- 성공 시 기대효과:
- 주요 리스크 및 대응방안:

### 5. 소요 예산 및 자원"""

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
    
    query = "우리 회사 실적이 급격히 나빠졌습니다. 종합 분석이 필요합니다."
    
    print(f"\n[초기 질문] {query}")
    
    recursive_analysis(router, agents_map, memory, query)
    
    final_solution = generate_final_solution(memory)
    print("\n" + final_solution)
    
    print("\n" + "=" * 60)
    print("분석 완료")
    print("=" * 60)

if __name__ == "__main__":
    main()