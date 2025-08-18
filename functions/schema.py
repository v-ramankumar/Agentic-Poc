
from typing import Literal, Optional, Any
from pydantic import BaseModel

# ---------- SCHEMAS ----------
class OutputSchemaPurpose(BaseModel):
    """Schema for Gemini's classification output."""
    Intent: Literal["pre_authorization","greetings", "status_check", "other"]
    patient_id: Optional[str]
    payer: Optional[Literal["cohere", "humana"]]
    # payer: Optional[str]
    # is_valid_payer: Optional[bool] = None

class PurposeClass(BaseModel):
    items: list[OutputSchemaPurpose]

class UserInput(BaseModel):
    query: str

class ResponseModel(BaseModel):
    status: Literal["success", "error", "incomplete"]
    message: str
    Intent: Optional[str] = None
    patient_id: Optional[str] = None
    payer: Optional[Any] = None
    # is_valid_payer: Optional[bool] = None
    data: Optional[Any] = None