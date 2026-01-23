class SharedMemory:
    def __init__(self):
        self.context = []
        self.max_context_length = 10
        self.summary_history = []
    
    def add(self, step, agent, content):
        entry = {
            "step": step,
            "agent": agent,
            "content": content,
            "timestamp": self._get_timestamp()
        }
        self.context.append(entry)
        
        if len(self.context) > self.max_context_length:
            self.summarize()
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def summarize(self):
        # 오래된 항목들을 요약
        old_entries = self.context[:-5]
        summary_text = f"[요약] {len(old_entries)}개 분석 완료: "
        
        agents_summary = {}
        for entry in old_entries:
            agent = entry['agent']
            if agent not in agents_summary:
                agents_summary[agent] = []
            agents_summary[agent].append(entry['content'][:50])
        
        for agent, contents in agents_summary.items():
            summary_text += f"{agent}({len(contents)}건) "
        
        self.summary_history.append(summary_text)
        self.context = self.context[-5:]
    
    def get_context(self):
        """최근 맥락 반환 (요약 이력 포함)"""
        result = []
        
        # 요약 이력 추가
        if self.summary_history:
            result.append("[이전 분석 요약]")
            result.extend(self.summary_history)
            result.append("")
        
        # 최근 분석 결과
        result.append("[최근 분석]")
        for c in self.context:
            result.append(f"[{c['agent'].upper()}] {c['content']}")
        
        return "\n".join(result)
    
    def get_by_agent(self, agent_name):
        """특정 에이전트의 분석만 반환"""
        return [c for c in self.context if c['agent'] == agent_name]
    
    def clear(self):
        self.context = []
        self.summary_history = []