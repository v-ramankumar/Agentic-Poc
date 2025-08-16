import json
from pydantic import BaseModel, Field

class n8nWebhookRequest(BaseModel):
    payer_id: str = Field(..., description="The ID of the payer")
    task: str = Field(..., description="The task to be performed")
    requestId: str = Field(..., description="The ID of the request")
    json_data: dict = Field(..., description="The JSON data to be processed")