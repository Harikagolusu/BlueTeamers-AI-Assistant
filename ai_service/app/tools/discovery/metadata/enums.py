from enum import Enum

class ToolCategory(str, Enum):
    SYSTEM = "SYSTEM"
    SECURITY = "SECURITY"
    NETWORK = "NETWORK"
    MITRE = "MITRE"
    UTILITY = "UTILITY"
    SEARCH = "SEARCH"
    DATABASE = "DATABASE"
    AI = "AI"
    CUSTOM = "CUSTOM"

class ToolState(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    EXPERIMENTAL = "EXPERIMENTAL"
    DEPRECATED = "DEPRECATED"
    INTERNAL = "INTERNAL"
