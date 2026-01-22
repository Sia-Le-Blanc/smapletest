class SharedMemory:
    def __init__(self):
        self.context = []
        self.max_context_length = 5
    
    def add(self, step, agent, content):
        entry = {
            "step": step,
            "agent": agent,
            "content": content
        }
        self.context.append(entry)
        
        if len(self.context) > self.max_context_length:
            self.summarize()
    
    def summarize(self):
        summary = f"[요약] 이전 {len(self.context)-2}개 단계 완료"
        self.context = self.context[-2:] + [{"step": "summary", "agent": "system", "content": summary}]
    
    def get_context(self):
        return "\n".join([f"[{c['agent']}] {c['content']}" for c in self.context])
    
    def clear(self):
        self.context = []