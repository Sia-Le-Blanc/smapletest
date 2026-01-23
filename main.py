# main.py
from router import Router
from agents import FinanceAgent, HRAgent, LegalAgent
from memory.shared_memory import SharedMemory

def main():
    router = Router()
    memory = SharedMemory()
    agents_map = {
        'finance': FinanceAgent(), 
        'hr': HRAgent(), 
        'legal': LegalAgent()
    }
    
    query = "회사의 매출 급감 및 사내 불만 증가에 대한 종합 분석"
    print(f"=== 분석 시작 ===")
    print(f"질문: {query}\n")
    
    current_round = 0
    
    # 1단계: 초기 부서 선택 및 분석
    selected = router.decide(query, "")
    print(f"[Round {current_round + 1}] 참여 부서: {', '.join(selected)}\n")
    
    for name in selected:
        print(f"  → {name.upper()} 분석 중...")
        result = agents_map[name].analyze(query, "")
        memory.add(current_round + 1, name, result)
    
    current_round += 1
    
    # 재귀 분석 (매 라운드마다 부서 재선택)
    while router.should_continue(memory.get_context(), current_round):
        debate_query = "타 부서 분석을 바탕으로 부서 간 충돌 지점과 연쇄 리스크를 분석하고, 통합 솔루션을 제시하세요."
        
        # 매 라운드마다 필요한 부서 재선택
        selected = router.decide(debate_query, memory.get_context())
        print(f"\n[Round {current_round + 1}] 참여 부서: {', '.join(selected)}")
        
        for name in selected:
            print(f"  → {name.upper()} 교차 분석 중...")
            result = agents_map[name].analyze(debate_query, memory.get_context())
            memory.add(current_round + 1, f"{name}_round{current_round + 1}", result)
        
        current_round += 1
    
    print(f"\n=== 분석 완료 (총 {current_round}라운드) ===\n")
    print(memory.get_context())

if __name__ == "__main__":
    main()