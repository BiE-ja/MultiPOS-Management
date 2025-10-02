from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str | None = None


class Sort(BaseModel):
    colum: str | None
    direction: str
