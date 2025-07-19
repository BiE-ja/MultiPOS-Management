
from sqlalchemy.orm import Session
from backend.app.core.security import verify_password
from backend.app.models.deps import User

def get_user_by_email(*, db : Session, email: str)-> User | None:
    return  db.query(User).filter(User.email == email).first()

def authenticate(*, session: Session, email:str, password : str)-> User | None:
    db_user = get_user_by_email(db = session, email = email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password): # type: ignore
        return None
    return db_user