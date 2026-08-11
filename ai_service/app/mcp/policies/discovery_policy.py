from enum import Enum

class DiscoveryPolicy(str, Enum):
    STATIC = "STATIC"       # Discovered once on startup
    ON_DEMAND = "ON_DEMAND" # Discovered when explicitly requested
    PERIODIC = "PERIODIC"   # Discovered on a scheduled interval
