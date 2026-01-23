from router import Router
from agents import FinanceAgent, HRAgent, LegalAgent
from memory.shared_memory import SharedMemory

def main():
    router = Router()
    memory = SharedMemory()
    agents_map = {'finance': FinanceAgent(), 'hr': HRAgent(), 'legal': LegalAgent()}
    
    query = "회사의 매출 급감 및 사내 불만 증가에 대한 종합 분석"
    
    # 1단계: 개별 현황 파악
    selected = router.decide(query, "")
    for name in selected:
        result = agents_map[name].analyze(query, "")
        memory.add(1, name, result)

    # 2단계: 상호 연계 토론 (9b 라우터 판단)
    if router.should_continue(memory.get_context()):
        debate_query = "타 부서 분석 결과를 바탕으로, 우리 부서에 닥칠 2차 연쇄 효과와 합동 대응책을 분석하세요."
        for name in selected:
            # memory.get_context()를 넘겨 기억 상실 방지
            result = agents_map[name].analyze(debate_query, memory.get_context())
            memory.add(2, f"{name}_debate", result)

    print(memory.get_context())

if __name__ == "__main__":
    main()