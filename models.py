from sqlalchemy import Column, Integer, String, Boolean, DateTime, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base, engine


class order(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    product_name= Column(String(255), nullable=False)
    brand= Column(String(255), nullable=False)
    price= Column(String(255), nullable=False)
    stock_status= Column(String(255), nullable=False)
    description= Column(String(1000),nullable=False)
    image= Column(String(255),nullable=False)
    audio= Column(String(255),nullable=False)
    video= Column(String(255),nullable=False)
    Status= Column(String(255),nullable=False)
    
    
class login(Base):
    __tablename__ ="signin"

    id = Column(Integer, primary_key=True, index=True)
    User = Column(String(30),nullable=False)
    Email = Column(String(255),nullable=False,unique=True)
    Phone_Number = Column(String(255),nullable=False,unique=True)
    Password = Column(String(128),nullable=False)    
    
    
class order22(Base):
    __tablename__ = 'complaints'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    description= Column(String(255),nullable=False)
    image= Column(String(255),nullable=False)
    
class order33(Base):
    __tablename__ = 'Payments'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    product_id= Column(Integer,nullable=False)
    name= Column(String(255),nullable=False)
    Address= Column(String(255),nullable=False)
    Pincode= Column(String(255),nullable=False)    
    Mobile_number= Column(String(255),nullable=False)
    quantity= Column(String(255),nullable=False)
    price=Column(String(255),nullable=False)

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    product_id= Column(Integer, nullable=False)
    user_name=Column(String(255),nullable=False)
    cart_Status= Column(String(255),nullable=False)


    Base.metadata.create_all(bind=engine)    