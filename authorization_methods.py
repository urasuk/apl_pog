from models import Session
from constants import *

def is_admin(model_class, uid):
    session = Session()
    return session.query(model_class).filter_by(uid=uid).one().userstatus == ADMIN

def uidFromOrder (model_class, order_id):
    session = Session()
    return session.query(model_class).filter_by(oid=order_id).one().userId