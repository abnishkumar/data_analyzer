from typing import List
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.Code_executor_agent import CodeExecutorAgentFactory
from agents.Data_analyzer_agent import DataAnalyzerAgentFactory

from config.constants import DEFAULT_MAX_TURNS, DEFAULT_TERMINATION_PHRASE

class DataAnalyzerTeamBuilder:
    """Factory for creating data analysis teams with proper configuration."""
    
    DEFAULT_MAX_TURNS = DEFAULT_MAX_TURNS
    DEFAULT_TERMINATION_PHRASE = DEFAULT_TERMINATION_PHRASE

    def __init__(self, docker_executor, model_client):
        """
        Args:
            docker_executor: Configured Docker executor
            model_client: Configured model client for analysis
        """
        self.docker = docker_executor
        self.model_client = model_client
        self._team = None

    def build_team(self) -> RoundRobinGroupChat:
        """Construct and return a configured analysis team"""
        code_executor = CodeExecutorAgentFactory.create(self.docker)
        data_analyzer = DataAnalyzerAgentFactory.create(self.model_client)

        termination = TextMentionTermination(self.DEFAULT_TERMINATION_PHRASE)

        self._team = RoundRobinGroupChat(
            participants=[data_analyzer, code_executor],
            max_turns=self.DEFAULT_MAX_TURNS,
            termination_condition=termination
        )
        return self._team

    @property
    def team(self) -> RoundRobinGroupChat:
        """Access the built team (lazy initialization)"""
        if self._team is None:
            return self.build_team()
        return self._team
