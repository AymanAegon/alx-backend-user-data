#!/usr/bin/env python3
""" User Module """
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """ The User class """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
