from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class RequestStatus(str, Enum):
    """Enumeration for request statuses."""
    CREATED = "created"
    VALIDATED = "validated"
    IN_PROGRESS = "in_progress"
    ACTION_NEEDED = "action_needed"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class RequestProgress(BaseModel):
    requestId: str = Field(..., description="Unique identifier for the request")
    status: RequestStatus = Field(..., description="Current status of the request")
    lastUpdatedAt: datetime = Field(..., description="Timestamp when the request was last updated")
    remarks: Optional[str] = Field(None, description="Remarks or comments related to the request")  
    
    class Config:
        use_enum_values = True