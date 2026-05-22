class PresentationAgentError(Exception):
    """Base exception for presentation-agent."""


class AgentGenerationError(PresentationAgentError):
    """Raised when OpenAI generation fails."""
