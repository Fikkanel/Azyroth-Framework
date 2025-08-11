from sqlalchemy import Column, Integer, String, Text
from .User import Base # Menggunakan Base dari model User yang sudah ada

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    project_link = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Project(title='{self.title}')>"
