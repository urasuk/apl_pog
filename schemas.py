from models import User, Category, Medicine, Order, OrdersMedicine
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ('uid', 'userstatus', 'username', 'firstname', 'lastname', 'email', 'password', 'phone')


class OrderSchema(Schema):
    class Meta:
        model = Order
        fields = ('oid', 'userId', 'shipDate', 'status')


class OrdersMedicineSchema(Schema):
    class Meta:
        model = OrdersMedicine
        fields = ('order_id', 'medicine_id')


class CategorySchema(Schema):
    class Meta:
        model = Category
        fields = ('cid', 'name')


class MedicineSchema(Schema):
    class Meta:
        model = Medicine
        fields = ('mid', 'category', 'name', 'manufacturer', 'status', 'demand')