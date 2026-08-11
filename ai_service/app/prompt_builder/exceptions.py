class PromptBuilderException(Exception):
    """Base exception for prompt builder errors."""
    pass

class TemplateNotFoundException(PromptBuilderException):
    pass

class TokenLimitExceededException(PromptBuilderException):
    pass
