import streamlit as st
from router import Router
from agents import FinanceAgent, HRAgent, LegalAgent
from memory.shared_memory import SharedMemory

st.set_page_config(page_title="Corporate Brain", layout="centered")
st.title("🏢 Corporate Brain: AI 전략 회의실")

if "memory" not in st.session_state:
    st.session_state.memory = SharedMemory() #
    st.session_state.router = Router()
    st.session_state.agents = {'finance': FinanceAgent(), 'hr': HRAgent(), 'legal': LegalAgent()}

if query := st.chat_input("이슈를 입력하세요 (예: 매출 급감 분석)"):
    st.session_state.memory.clear()
    
    with st.status("비서실장(9b)이 분석 방향을 설정 중...") as status:
        selected = st.session_state.router.decide(query, "")
        st.write(f"✅ 참여 부서: {', '.join(selected)}")
        
        # 1차 분석 진행
        for name in selected:
            st.write(f"🏃 {name.upper()} 팀 현황 분석 중...")
            res = st.session_state.agents[name].analyze(query, "")
            st.session_state.memory.add(1, name, res)
        
        # 2차 교차 토론 진행
        if st.session_state.router.should_continue(st.session_state.memory.get_context()):
            st.write("🔄 **심화 분석:** 부서 간 연쇄 리스크 토론을 시작합니다.")
            debate_query = "타 부서 분석 결과가 미칠 도미노 효과를 분석하세요."
            for name in selected:
                res = st.session_state.agents[name].analyze(debate_query, st.session_state.memory.get_context())
                st.session_state.memory.add(2, f"{name}_debate", res)
        
        status.update(label="전략 도출 완료", state="complete")

    # 결과 표시
    for item in st.session_state.memory.context:
        with st.chat_message(item['agent']):
            st.write(f"**[{item['agent'].upper()}]**")
            st.write(item['content'])