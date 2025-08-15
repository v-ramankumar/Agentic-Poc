from pydantic import BaseModel, Field , Optional
from dbmodels.utility import httpResponseEnum

class JsonValidatorResponse(BaseModel):
    is_valid: bool = Field(..., description="Indicates if the JSON data is valid")
    http_status: httpResponseEnum = Field(..., description="The HTTP status of the response")
    error_message: Optional[str] = Field(None, description="Error message if any")