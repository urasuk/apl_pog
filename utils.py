def update_util(model, data):
    try:
        if data.get('username', None):
            model.username = data['username']
        if data.get('password', None):
            model.password = data['password']
        if data.get('firstname', None):
            model.firstname = data['firstname']
        if data.get('lastname', None):
            model.lastname = data['lastname']
        if data.get('email', None):
            model.email = data['email']
        if data.get('phone', None):
            model.phone = data['phone']
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
