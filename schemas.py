from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class GitHubLabel(BaseModel):
    name: str
    color: str

class GitHubIssue(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    number: int
    title: str
    body: Optional[str] = None
    state: str
    html_url: str
    updated_at: datetime
    labels: List[GitHubLabel] = []