import datetime
from sqlalchemy.orm import Session

from repository.engine import engine
from repository.models.message import Message
from repository.models.user import User

session = Session(engine)

def create_message(text: str, user_id: str) -> Message:
    timestamp = str(int(datetime.datetime.utcnow().timestamp()))
    sender = session.query(User).filter_by(id=user_id).first()
    new_message = Message(text=text, sender=sender, timestamp=timestamp)
    session.add(new_message)
    session.commit()
    return new_message

def delete_message(id: str) -> None:
    message = session.query(Message).filter_by(id=id).first()
    if message:
        session.delete(message)
        session.commit()

def get_messages_from_user(user_id: str) -> list:
    return session.query(Message).filter_by(user_id=user_id).all()