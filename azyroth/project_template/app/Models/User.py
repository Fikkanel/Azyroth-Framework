from sqlalchemy.orm import declarative_base, relationship # Pastikan relationship diimpor
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return f"<User(name='{self.name}')>"
