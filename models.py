from sqlalchemy import (
    Table,
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

#engine = create_engine('mysql://root:sqlLp9lp@localhost:3306/pharmacy')
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/pharmacy')

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
    userstatus = Column(String(5), nullable=False)
    username = Column(String(10), nullable=False)
    firstname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False)
    password = Column(String(100), nullable=False)
    phone = Column(String(10), nullable=False)


    def __str__(self):
        return f"User id: {self.uid}\n" \
               f"User status: {self.userstatus}\n" \
               f": {self.uid}\n" \
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



OrdersMedicine = Table('orders_medicine', BaseModel.metadata,
                       Column('order_id', ForeignKey('orders.oid')),
                       Column('medicine_id', ForeignKey('medicine.mid')),
                      # quantity=Column(Integer, nullable=False)
                       )


class Medicine(BaseModel):
    __tablename__ = "medicine"

    mid = Column(Integer(), primary_key=True)
    category = Column(Integer, ForeignKey(Category.cid))
    name = Column(String(30))
    manufacturer = Column(String(30))
    status = Column(String(30))
    demand = Column(Boolean)
    orders = relationship("Order", secondary=OrdersMedicine, back_populates="medicine")

    def __str__(self):
        return f"Medicine id: {self.mid}\n" \
               f"Category: {self.category}\n" \
               f"Name: {self.name}\n" \
               f"Manufacturer: {self.manufacturer}\n" \
               f"Status: {self.status}\n" \
               f"Demand: {self.demand}\n" \


class Order(BaseModel):
    __tablename__ = "orders"

    oid = Column(Integer(), primary_key=True)
    userId = Column(Integer, ForeignKey('user.uid'))
    shipDate = Column(DateTime(6))
    status = Column(String(30))
    medicine = relationship("Medicine", secondary=OrdersMedicine, back_populates="orders")

    def __str__(self):
        return f"Order id: {self.oid}\n" \
               f"User id: {self.userId}\n" \
               f"Ship date: {self.shipDate}\n" \
               f"Status: {self.status}\n"


