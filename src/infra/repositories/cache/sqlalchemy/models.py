from sqlalchemy import Column, Integer, Boolean, String, Float
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

class SegmentoModel(Base):
  __tablename__ = "segmentos"

  id = Column(Integer, primary_key=True, autoincrement=True)
  protocolo_id = Column(Integer, nullable=False)
  obra_id = Column(Integer, nullable=False)
  geometria = Column(String, nullable=False)
  cor = Column(Integer, nullable=False)
  data = Column(String, nullable=False)  # Store as ISO format string