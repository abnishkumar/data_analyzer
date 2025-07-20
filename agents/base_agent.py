from abc import ABC, abstractmethod
from typing import Any
from autogen_agentchat.agents import CodeExecutorAgent

class BaseAgentFactory(ABC):
    """Abstract base class for agent factories"""
    
    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> Any:
        """Create and return an agent instance"""
        raise NotImplementedError