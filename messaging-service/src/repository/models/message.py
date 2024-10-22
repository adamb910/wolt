from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from repository.models.base import Base

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey('users.id'))
    text: Mapped[str] = mapped_column(String(64))
    timestamp: Mapped[str] = mapped_column(String(10)) # stored as a string to keep it simple :)
    sender = relationship('User', back_populates='messages')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.text,
            "email": self.timestamp,
            "sender": self.sender.name
        }