import os
import asyncio
from dotenv import load_dotenv
from router import Router
from agents import FinanceAgent, HRAgent, LegalAgent
from memory.shared_memory import SharedMemory

load_dotenv()

async def run_agent(agent, name, query, context):
    print(f"  → {name} 분석 시작...")
    result = agent.analyze(query, context)
    print(f"  ✓ {name} 완료")
    return name, result

async def recursive_analysis(router, agents_map, memory, query, depth=0):
    print(f"\n{'  ' * depth}[Depth {depth+1}: Router Decision]")
    selected = router.decide(query, memory.get_context())
    print(f"{'  ' * depth}  선택된 전문가: {', '.join(selected)}")
    
    print(f"{'  ' * depth}[Depth {depth+1}: Agent Execution]")
    tasks = [run_agent(agents_map[agent], agent, query, memory.get_context()) 
             for agent in selected if agent in agents_map]
    
    results = await asyncio.gather(*tasks)
    
    for name, result in results:
        print(f"\n{'  ' * depth}[{name.upper()} 결과]")
        print(f"{'  ' * depth}{result[:200]}...")
        memory.add(depth+1, name, result)
    
    print(f"\n{'  ' * depth}[Router 종료 판단 중...]")
    if router.should_continue(memory.get_context()):
        print(f"{'  ' * depth}  → 추가 분석 필요")
        await recursive_analysis(router, agents_map, memory, "이전 분석을 심화하여 최종 전략 도출", depth+1)
    else:
        print(f"{'  ' * depth}  → 분석 충분, 종료")

async def main():
    print("=" * 60)
    print("Corporate Brain System (자동 종료 판단)")
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
    
    await recursive_analysis(router, agents_map, memory, query)
    
    print("\n" + "=" * 60)
    print("최종 분석 완료")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())