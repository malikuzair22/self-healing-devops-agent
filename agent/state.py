from typing import TypedDict, Optional


class AgentState(TypedDict):
    incident_id: str
    source : str
    logs : str
    metrics: str
    diagnosis: Optional[str]
    confidence: Optional[float]
    action_taken: Optional[str]
    status: Optional[str]
    pod_name: Optional[str]





