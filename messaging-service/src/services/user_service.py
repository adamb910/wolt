from sqlalchemy.orm import Session

from repository.engine import engine
from repository.models.user import User

session = Session(engine)

def get_users(email_filter: str) -> list:
    if email_filter:
        users = session.query(User).filter_by(email=email_filter).all()
    else:
        users = session.query(User).all()
    return users

def create_user(name: str, email: str) -> User:
    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()
    return new_user

def update_user(id: int, name: str, email: str) -> User:
    user = session.query(User).filter_by(id=id).first()
    if user:
        user.name = name
        user.email = email
        session.commit()
    return user

def delete_user(id: int) -> None:
    user = session.query(User).filter_by(id=id).first()
    if user:
        session.delete(user)
        session.commit()