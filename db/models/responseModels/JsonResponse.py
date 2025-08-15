from pydantic import BaseModel, Field,Optional
from dbmodels.utility import httpResponseEnum
class JsonResponse(BaseModel):
    json_data: dict = Field(..., description="The JSON data to be returned")
    http_status: httpResponseEnum = Field(..., description="The HTTP status of the response")
    error_message: Optional[str] = Field(None, description="Error message if any")