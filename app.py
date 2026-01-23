# app.py
import streamlit as st
from router import Router
from agents import FinanceAgent, HRAgent, LegalAgent
from memory.shared_memory import SharedMemory

# 페이지 설정
st.set_page_config(
    page_title="홍익AI - 기업을 널리 이롭게 하라",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 로드
def load_css():
    try:
        with open('styles.css', 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# 세션 상태 초기화
if "memory" not in st.session_state:
    st.session_state.memory = SharedMemory()
    st.session_state.router = Router()
    st.session_state.agents = {
        'finance': FinanceAgent(), 
        'hr': HRAgent(), 
        'legal': LegalAgent()
    }
    st.session_state.analysis_done = False
    st.session_state.round_count = 0
    st.session_state.dept_summaries = {}

# --- 헤더 영역 ---
# 상단 타이틀
st.markdown('<h1 class="title">✨ 홍익AI</h1>', unsafe_allow_html=True)
# 슬로건 추가
st.markdown('<p class="slogan">기업을 널리 이롭게 하라</p>', unsafe_allow_html=True)
# 서브타이틀
st.markdown('<p class="subtitle">AI 기반 전사 통합 분석 및 의사결정 지원 시스템</p>', unsafe_allow_html=True)

# --- 검색 및 분석 영역 ---
_, center_col, _ = st.columns([1, 5, 1])

with center_col:
    query = st.text_input(
        "분석 질문 입력",
        placeholder="분석하고 싶은 기업 이슈를 입력하세요...",
        label_visibility="collapsed"
    )
    analyze_btn = st.button("🚀 지능형 분석 시작", use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# 분석 실행 로직
if analyze_btn and query:
    st.session_state.memory.clear()
    st.session_state.analysis_done = False
    st.session_state.round_count = 0
    st.session_state.dept_summaries = {'finance': [], 'hr': [], 'legal': []}
    
    with st.status("🤖 홍익AI 엔진이 데이터를 교차 분석하고 있습니다...", expanded=True) as status:
        selected = st.session_state.router.decide(query, "")
        st.write(f"🎯 **참여 부서 확정:** {', '.join([d.upper() for d in selected])}")
        st.session_state.round_count += 1
        
        # Round 1 분석
        st.write(f"\n### 📊 Round {st.session_state.round_count}: 개별 현황 정밀 진단")
        for name in selected:
            with st.spinner(f"{name.upper()} 분석 중..."):
                result = st.session_state.agents[name].analyze(query, "")
                st.session_state.memory.add(st.session_state.round_count, name, result)
                
                summary_lines = [line for line in result.split('\n') if line.strip()]
                summary = summary_lines[0][:200] + "..." if summary_lines else ""
                st.session_state.dept_summaries[name].append({
                    'round': st.session_state.round_count,
                    'summary': summary
                })
        
        # 교차 분석 (Recursive)
        while st.session_state.router.should_continue(
            st.session_state.memory.get_context(), 
            st.session_state.round_count
        ):
            st.session_state.round_count += 1
            debate_query = "타 부서 분석을 바탕으로 부서 간 충돌 지점과 연쇄 리스크를 분석하고, 통합 솔루션을 제시하세요."
            selected = st.session_state.router.decide(debate_query, st.session_state.memory.get_context())
            
            st.write(f"\n### 🔄 Round {st.session_state.round_count}: 부서 간 교차 분석")
            for name in selected:
                with st.spinner(f"{name.upper()} 교차 분석 중..."):
                    result = st.session_state.agents[name].analyze(debate_query, st.session_state.memory.get_context())
                    st.session_state.memory.add(st.session_state.round_count, f"{name}_r{st.session_state.round_count}", result)
                    
                    summary_lines = [line for line in result.split('\n') if line.strip()]
                    summary = summary_lines[0][:200] + "..." if summary_lines else ""
                    st.session_state.dept_summaries[name].append({
                        'round': st.session_state.round_count,
                        'summary': summary
                    })
        
        status.update(label=f"✅ 분석 완료 (총 {st.session_state.round_count} 라운드)", state="complete")
    st.session_state.analysis_done = True

# --- 결과 리포트 영역 ---
if st.session_state.analysis_done:
    st.markdown('<h2 style="text-align:center; margin-bottom:40px; font-weight:800;">📌 부서별 통합 요약</h2>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    dept_info = {
        'finance': {'name': '💰 재무 인사이트', 'color': '#4f46e5'},
        'hr': {'name': '👥 조직/인사 전략', 'color': '#7c3aed'},
        'legal': {'name': '⚖️ 법무 리스크 관리', 'color': '#2563eb'}
    }
    
    for idx, (dept, info) in enumerate(dept_info.items()):
        with cols[idx]:
            if dept in st.session_state.dept_summaries and st.session_state.dept_summaries[dept]:
                last_summary = st.session_state.dept_summaries[dept][-1]['summary'].replace('<', '&lt;').replace('>', '&gt;')
                st.markdown(f"""
                <div class="dept-card" style="border-top: 5px solid {info['color']}">
                    <div class="dept-name">{info['name']}</div>
                    <div class="dept-summary">
                        {last_summary[:160]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="dept-card" style="opacity: 0.4;"><div class="dept-name">{info["name"]}</div>분석 제외됨</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📋 상세 분석 타임라인")
    
    rounds = {}
    for item in st.session_state.memory.context:
        r_num = item['step']
        if r_num not in rounds: rounds[r_num] = []
        rounds[r_num].append(item)
    
    for r_num in sorted(rounds.keys()):
        with st.expander(f"🔍 Round {r_num} 분석 데이터", expanded=(r_num == 1)):
            for item in rounds[r_num]:
                st.markdown(f"### {item['agent'].upper()}")
                st.markdown(item['content'])
                st.markdown("---")