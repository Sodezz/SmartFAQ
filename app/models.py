from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

basemodel = declarative_base()

class Document(basemodel):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

