# app.py
import streamlit as st
from router import Router
from agents import FinanceAgent, HRAgent, LegalAgent
from memory.shared_memory import SharedMemory

# 페이지 설정
st.set_page_config(
    page_title="Corporate Brain AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 로드
def load_css():
    with open('styles.css', 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# 초기화
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

# 헤더
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="title">🧠 Corporate Brain AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI 기반 전사 통합 분석 시스템</p>', unsafe_allow_html=True)

# 검색 영역
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "",
        placeholder="예: 매출 급감과 직원 불만 증가 원인 분석",
        label_visibility="collapsed"
    )

with col2:
    analyze_btn = st.button("🚀 분석 시작", use_container_width=True)

st.markdown("---")

# 분석 실행
if analyze_btn and query:
    st.session_state.memory.clear()
    st.session_state.analysis_done = False
    st.session_state.round_count = 0
    st.session_state.dept_summaries = {'finance': [], 'hr': [], 'legal': []}
    
    with st.status("🤖 AI가 전사 데이터를 분석하고 있습니다...", expanded=True) as status:
        # 초기 부서 선택
        selected = st.session_state.router.decide(query, "")
        st.write(f"✅ **참여 부서:** {', '.join([d.upper() for d in selected])}")
        st.session_state.round_count += 1
        
        # 1차 분석
        st.write(f"\n### 📊 Round {st.session_state.round_count}: 개별 부서 현황 분석")
        for name in selected:
            with st.spinner(f"{name.upper()} 팀 분석 중..."):
                result = st.session_state.agents[name].analyze(query, "")
                st.session_state.memory.add(st.session_state.round_count, name, result)
                # 요약 저장 (첫 200자)
                summary_lines = [line for line in result.split('\n') if line.strip()]
                summary = summary_lines[0][:200] + "..." if summary_lines else ""
                st.session_state.dept_summaries[name].append({
                    'round': st.session_state.round_count,
                    'summary': summary
                })
                st.success(f"✓ {name.upper()} 분석 완료")
        
        # 재귀 분석
        while st.session_state.router.should_continue(
            st.session_state.memory.get_context(), 
            st.session_state.round_count
        ):
            st.session_state.round_count += 1
            
            debate_query = "타 부서 분석을 바탕으로 부서 간 충돌 지점과 연쇄 리스크를 분석하고, 통합 솔루션을 제시하세요."
            
            selected = st.session_state.router.decide(
                debate_query, 
                st.session_state.memory.get_context()
            )
            
            st.write(f"\n### 🔄 Round {st.session_state.round_count}: 부서 간 교차 분석")
            st.write(f"✅ **참여 부서:** {', '.join([d.upper() for d in selected])}")
            
            for name in selected:
                with st.spinner(f"{name.upper()} 교차 분석 중..."):
                    result = st.session_state.agents[name].analyze(
                        debate_query, 
                        st.session_state.memory.get_context()
                    )
                    st.session_state.memory.add(
                        st.session_state.round_count, 
                        f"{name}_r{st.session_state.round_count}", 
                        result
                    )
                    # 요약 저장
                    summary_lines = [line for line in result.split('\n') if line.strip()]
                    summary = summary_lines[0][:200] + "..." if summary_lines else ""
                    st.session_state.dept_summaries[name].append({
                        'round': st.session_state.round_count,
                        'summary': summary
                    })
                    st.success(f"✓ {name.upper()} 교차분석 완료")
        
        status.update(
            label=f"✅ 분석 완료 (총 {st.session_state.round_count} 라운드)", 
            state="complete"
        )
    
    st.session_state.analysis_done = True

# 결과 표시
if st.session_state.analysis_done:
    st.markdown("---")
    
    # 부서별 요약 카드
    st.markdown("## 📌 부서별 분석 요약")
    
    cols = st.columns(3)
    dept_info = {
        'finance': {'name': '💰 재무팀', 'color': '#667eea'},
        'hr': {'name': '👥 인사팀', 'color': '#f093fb'},
        'legal': {'name': '⚖️ 법무팀', 'color': '#4facfe'}
    }
    
    for idx, (dept, info) in enumerate(dept_info.items()):
        with cols[idx]:
            if dept in st.session_state.dept_summaries and st.session_state.dept_summaries[dept]:
                last_summary = st.session_state.dept_summaries[dept][-1]['summary']
                # HTML 특수문자 이스케이프
                last_summary = last_summary.replace('<', '&lt;').replace('>', '&gt;')
                
                st.markdown(f"""
                <div class="dept-card">
                    <div class="dept-name">{info['name']}</div>
                    <div class="dept-summary">
                        <strong>분석 횟수:</strong> {len(st.session_state.dept_summaries[dept])}회<br><br>
                        <strong>최종 의견:</strong><br>
                        {last_summary[:150]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="dept-card">
                    <div class="dept-name">{info['name']}</div>
                    <div class="dept-summary">
                        이번 분석에 참여하지 않음
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 전체 분석 결과
    st.markdown("## 📋 상세 분석 결과")
    
    # 라운드별로 그룹화
    rounds = {}
    for item in st.session_state.memory.context:
        round_num = item['step']
        if round_num not in rounds:
            rounds[round_num] = []
        rounds[round_num].append(item)
    
    for round_num in sorted(rounds.keys()):
        with st.expander(f"🔍 Round {round_num} 분석 내용", expanded=(round_num == 1)):
            for item in rounds[round_num]:
                agent_name = item['agent'].upper().replace('_R', ' (Round ')
                if '_r' in item['agent']:
                    agent_name += ')'
                
                # 부서별 아이콘
                base_agent = item['agent'].split('_')[0].upper()
                icon = {'FINANCE': '💰', 'HR': '👥', 'LEGAL': '⚖️'}.get(base_agent, '📊')
                
                st.markdown(f"### {icon} {agent_name}")
                st.markdown(f"⏰ {item['timestamp']}")
                st.markdown(item['content'])
                st.markdown("---")
    
    # 다운로드 버튼
    full_report = f"""# Corporate Brain AI 분석 보고서

## 질의: {query}
## 분석 일시: {st.session_state.memory.context[0]['timestamp']}
## 총 분석 라운드: {st.session_state.round_count}

---

{st.session_state.memory.get_context()}
"""
    
    st.download_button(
        label="📥 전체 보고서 다운로드 (Markdown)",
        data=full_report,
        file_name=f"corporate_brain_report_{st.session_state.memory.context[0]['timestamp'].replace(':', '-')}.md",
        mime="text/markdown",
        use_container_width=True
    )

st.markdown('</div>', unsafe_allow_html=True)