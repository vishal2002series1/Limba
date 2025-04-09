from pydantic import BaseModel, Field
from typing import Optional

class AuthSchema(BaseModel):
    username: str
    password: str