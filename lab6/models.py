from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Boolean,
    DateTime
)
# from sqlalchemy import orm
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
import sys
sys.path.append(r"C:\Users\Kcюша\pcode\pp_project\lab6")

engine = create_engine('mysql://root:mySQL.kt.1502@localhost:3306/lab6_database')

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

BaseModel = declarative_base()


# class MEnum(enum.Enum):
#     available = "available"
#     pending = "pending"
#     unavailable = "unavailable"
#
#
# class OEnum(enum.Enum):
#     placed = "placed"
#     approved = "approved"
#     delivered = "delivered"


class User(BaseModel):
    __tablename__ = "user"

    uid = Column(Integer(), primary_key=True)
    username = Column(String(30))
    firstname = Column(String(30))
    lastname = Column(String(30))
    email = Column(String(30))
    password = Column(String(15))
    phone = Column(String(15))

    def __str__(self):
        return f"User id: {self.uid}\n" \
               f"Username: {self.username}\n" \
               f"Name: {self.firstname}\n" \
               f"Lastname: {self.lastname}\n" \
               f"Email: {self.email}\n" \
               f"Password: {self.password}\n" \
               f"Phone: {self.phone}\n" \



class Category(BaseModel):
    __tablename__ = "category"

    cid = Column(Integer(), primary_key=True)
    name = Column(String(30))

    def __str__(self):
        return f"Category id: {self.cid}\n" \
               f"Name: {self.name}\n" \



class OrdersMedicine(BaseModel):
    __tablename__ = 'orders_medicine'

    order_id = Column(Integer, ForeignKey('order.oid'))
    medicine_id = Column(Integer, ForeignKey('medicine.mid'))

    order = relationship("Order")
    medicine = relationship("Medicine")


class Medicine(BaseModel):
    __tablename__ = "medicine"

    mid = Column(Integer(), primary_key=True)
    category = Column(Integer, ForeignKey(Category.cid))
    name = Column(String(30))
    manufacturer = Column(String(30))
    status = Column(String(30))
    demand = Column(Boolean)

    def __str__(self):
        return f"Medicine id: {self.mid}\n" \
               f"Category: {self.category}\n" \
               f"Name: {self.name}\n" \
               f"Manufacturer: {self.manufacturer}\n" \
               f"Status: {self.status}\n" \
               f"Demand: {self.demand}\n" \



class Order(BaseModel):
    __tablename__ = "order"

    oid = Column(Integer(), primary_key=True)
    userId = Column(Integer, ForeignKey('user.uid'))
    quantity = Column(Integer())
    shipDate = Column(DateTime(6))
    status = Column(String(30))
    complete = Column(Boolean)
    medicine = relationship("Medicine", secondary=OrdersMedicine)

    def __str__(self):
        return f"Order id: {self.oid}\n" \
               f"User id: {self.userId}\n" \
               f"Quantity: {self.quantity}\n" \
               f"Ship date: {self.shipDate}\n" \
               f"Status: {self.status}\n" \
               f"Complete: {self.complete}\n" \
