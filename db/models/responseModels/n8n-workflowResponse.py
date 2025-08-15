from pydantic import BaseModel, Field
from dbmodels.utility import httpResponseEnum

class N8nWorkflowResponse(BaseModel):
    http_status: httpResponseEnum = Field(..., description="The HTTP status of the response")
    error_message: Optional[str] = Field(None, description="Error message if any")
    