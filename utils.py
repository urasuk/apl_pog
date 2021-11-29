from models import Session, User


def find_by_id(model, id):
    session = Session()
    try:
        t = session.query(model).filter_by(uid=id).one()
    except:
        return None
    return t


def update_util(model, data):
    try:
        if data.get('username', None):
            model.userName = data['userName']
        if data.get('password', None):
            model.password = data['password']
        if data.get('firstname', None):
            model.firstName = data['firstName']
        if data.get('lastname', None):
            model.lastName = data['lastName']
        if data.get('email', None):
            model.email = data['email']
        if data.get('phone', None):
            model.phone = data['phone']
        if data.get('uid', None):
            model.Id = data['uid']
        if data.get('category', None):
            model.category = data['category']
        if data.get('status', None):
            model.status = data['status']
        if data.get('manufacturer', None):
            model.manufacturer = data['manufacturer']
        if data.get('name', None):
            model.name = data['name']
    except:
        return None

    return model
