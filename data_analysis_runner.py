from typing import AsyncGenerator, Optional
from models.openai_model_client import ModelClient
from teams.data_analyzer_team import DataAnalyzerTeamBuilder
from autogen_agentchat.messages import TextMessage

from config.docker_util import (
    getDockerCommandLineExecutor,
    start_docker_container,
    stop_docker_container
)
from autogen_agentchat.messages import TextMessage
import logging


class DataAnalysisRunner:
    """
    Orchestrates the lifecycle of a data analysis task using a Docker environment,
    a model client, and a data analysis agent team.
    """

    def __init__(self) -> None:
        self.docker: Optional[object] = None
        self.team: Optional[object] = None
        self.model_client: Optional[ModelClient] = None
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self) -> "DataAnalysisRunner":
        """Set up resources like model client, Docker, and team."""
        try:
            self.logger.info("Initializing DataAnalysisRunner...")

            self.model_client = ModelClient.get_client()
            self.docker = getDockerCommandLineExecutor()
            self.team = DataAnalyzerTeamBuilder(self.docker, self.model_client).team

            self.logger.info("Starting Docker container...")
            await start_docker_container(self.docker)

            self.logger.info("DataAnalysisRunner initialized successfully.")
            return self

        except Exception as e:
            self.logger.error("Initialization failed: %s", e, exc_info=True)
            await self._cleanup_resources()
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Ensure all resources are cleaned up after task completion or failure."""
        await self._cleanup_resources()

        if exc_type:
            self.logger.error("Analysis error occurred: %s", exc_val, exc_info=True)

    async def _cleanup_resources(self) -> None:
        """Stop and clean up Docker container if running."""
        if self.docker:
            try:
                self.logger.info("Stopping Docker container...")
                await stop_docker_container(self.docker)
                self.logger.info("Docker container stopped.")
            except Exception as e:
                self.logger.warning("Failed to stop Docker container: %s", e, exc_info=True)

    async def analyze_data(self, task: str) -> AsyncGenerator[TextMessage, None]:
        try:
            self.logger.info("Starting task: %s", task)
            async for result in self.team.run_stream(task=task):
                if isinstance(result, TextMessage):
                    yield result
        except Exception as e:
            self.logger.error("Analysis failed: %s", e, exc_info=True)
            raise
        finally:
            self.logger.info("Task completed: %s", task)

