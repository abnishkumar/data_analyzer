from typing import Any
from autogen_agentchat.agents import CodeExecutorAgent

from agents.base_agent import BaseAgentFactory




class CodeExecutorAgentFactory(BaseAgentFactory):
    """Factory for creating CodeExecutorAgent instances with consistent configuration"""
    
    DEFAULT_NAME = 'Python_Code_Executor'
    
    @classmethod
    def create(cls, 
              code_executor: Any,
              name: str = DEFAULT_NAME,
              **kwargs) -> CodeExecutorAgent:
        """
        Create a configured CodeExecutorAgent instance
        
        Args:
            code_executor: The code executor implementation
            name: Name for the agent (default: 'Python_Code_Executor')
            **kwargs: Additional arguments to pass to CodeExecutorAgent
            
        Returns:
            Configured CodeExecutorAgent instance
        """
        return CodeExecutorAgent(
            name=name,
            code_executor=code_executor,
            **kwargs
        )


# Example usage:
# executor = SomeCodeExecutor()
# agent = CodeExecutorAgentFactory.create(executor)
# agent_with_custom_name = CodeExecutorAgentFactory.create(executor, name="Custom_Executor")