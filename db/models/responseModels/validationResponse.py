from pydantic import BaseModel, Field
from dbmodels.utility import httpResponseEnum
class ValidationResponse(BaseModel):
    message:str = Field(..., description="The message of the response")
    http_status: httpResponseEnum = Field(..., description="The HTTP status of the response")   
    error_message:Optional[str] = Field(None, description="Error message if any")