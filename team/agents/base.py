from swarm import Swarm, Agent
from typing import List, Dict, Any

class AgentWithMemory:
    def __init__(self, agent, max_memory=10):
        self.agent = agent
        self.memory = []
        self.max_memory = max_memory
        self.last_search_results = []
        self.last_content_results = []
    
    def add_to_memory(self, message):
        self.memory.append(message)
        # Keep only the last max_memory messages
        if len(self.memory) > self.max_memory:
            self.memory = self.memory[-self.max_memory:]
    
    def get_memory(self):
        return self.memory 