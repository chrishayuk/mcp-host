# models.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class ResponseModel(BaseModel):
    status: str
    message: str

class TabInfo(BaseModel):
    index: int
    name: str
    url: str

class TabResponse(BaseModel):
    status: str
    tabs: List[TabInfo]

class AlertAction(BaseModel):
    action: str = Field(..., pattern="^(accept|dismiss)$")
    prompt_text: Optional[str] = None

    @validator("action")
    def check_action(cls, value):
        if value not in ["accept", "dismiss"]:
            raise ValueError("Invalid action. Use 'accept' or 'dismiss'")
        return value
