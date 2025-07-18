from backend.app.database import Base

class Message (Base):
    message: str

class Token(Base):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(Base):
    sub: str | None = None

class NewPassword(Base):
    token: str
    new_password: str

        