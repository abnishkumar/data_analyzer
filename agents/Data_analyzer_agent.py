from dataclasses import dataclass
from typing import Optional, Any
from autogen_agentchat.agents import AssistantAgent
from agents.base_agent import BaseAgentFactory
from agents.prompts.data_analyzer_message import DATA_ANALYZER_SYSTEM_MESSAGE

@dataclass
class DataAnalyzerConfig:
    """Configuration for Data Analyzer Agent"""
    name: str = "Data_Analyzer_agent"
    description: str = "An Agent that solves Data Analysis problems and provides the code"
    system_message: str = DATA_ANALYZER_SYSTEM_MESSAGE

class DataAnalyzerAgentFactory(BaseAgentFactory):
    """Factory for creating configured Data Analyzer AssistantAgents"""
    
    _default_config = DataAnalyzerConfig()

    @classmethod
    def create(
        cls,
        model_client: Any,
        name: Optional[str] = None,
        description: Optional[str] = None,
        system_message: Optional[str] = None,
        **kwargs
    ) -> AssistantAgent:
        """
        Create a configured AssistantAgent for data analysis
        
        Args:
            model_client: The model client to use
            name: Optional agent name (default: "Data_Analyzer_agent")
            description: Optional agent description
            system_message: Optional system message override
            **kwargs: Additional arguments to pass to AssistantAgent
            
        Returns:
            Configured AssistantAgent instance
        """
        config = cls._default_config
        
        return AssistantAgent(
            name=name or config.name,
            model_client=model_client,
            description=description or config.description,
            system_message=system_message or config.system_message,
            **kwargs
        )