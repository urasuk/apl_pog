from flask import Flask, request, jsonify
from models import Session, User
from constants import *
from schemas import *
from utils import *
from flask_httpauth import HTTPBasicAuth
from authorization_methods import *

import bcrypt

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    session = Session()
    try:
        user_to_check = session.query(User).filter_by(username=username).one()
    except:
        return jsonify(INCORRECT_USERNAME), 401

    try:
        if bcrypt.checkpw(password.encode('utf-8'), user_to_check.password.encode('utf-8')):
            return user_to_check.uid, 200

        else:
            return jsonify(BAD_PASSWORD), 401
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


# All about user
@app.route(BASE_PATH + USER_PATH, methods=['POST'])
def create_user():
    try:
        user_data = request.get_json()
        session = Session()
        try:
            if session.query(User).filter_by(uid=user_data.get('uid')).one():
                return jsonify(USER_ALREADY_EXISTS), 409
        except:
            pass
        new_user = User(**user_data)
        # password hashing ------------------------------------
        passwd = user_data.get('password')
        b = bytes(passwd, 'utf-8')
        hashed_password = bcrypt.hashpw(b, bcrypt.gensalt())
        # -----------------------------------------------------
        new_user.password = hashed_password
        session.add(new_user)
        session.commit()
        return jsonify(USER_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + USER_PATH + '/' + '<int:Id>', methods=['GET'])
@auth.login_required()
def get_user_by_userId(Id):
    current = auth.current_user()

    if current[1] != 200:
        return current

    session = Session()
    current_o = session.query(User).filter_by(uid=current[0]).one()

    if current_o.userstatus == ADMIN or current_o.uid == Id:
        try:
            user = session.query(User).filter_by(uid=Id).one()
        except:
            return jsonify(USER_NOT_FOUND), 404

        return jsonify(UserSchema().dump(user)), 200

    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + USER_PATH, methods=['GET'])
@auth.login_required()
def get_all_users():
    current = auth.current_user()

    if current[1] != 200:
        return current

    session = Session()
    if session.query(User).filter_by(uid=current[0]).one().userstatus == ADMIN:
        try:
            users = session.query(User).all()
        except:
            users = []

        users_dto = UserSchema(many=True)
        return jsonify(users_dto.dump(users)), 200
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + USER_PATH + '/' + '<int:Id>', methods=['PUT'])
@auth.login_required()
def update_user(Id):
    current = auth.current_user()
    session = Session()

    if current[1] != 200:
        return current

    if current[0] != Id:
        return jsonify(ACCESS_DENIED), 403

    try:
        if request.json['uid']:
            return jsonify(CANT_CHANGE_ID), 400
    except:
        pass
    try:
        update_request = request.get_json()
        user = session.query(User).filter_by(uid=Id).one()
        if update_request.get('password'):
            # password hashing ------------------------------------
            password = update_request.get('password')
            b = bytes(password, 'utf-8')
            hashed_password = bcrypt.hashpw(b, bcrypt.gensalt())
            update_request['password'] = hashed_password
            # -----------------------------------------------------

        update_user = update_util(user, update_request)

        if update_user == None:
            return jsonify(SOMETHING_WENT_WRONG), 400
        session.commit()
        return jsonify(USER_UPDATED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + USER_PATH + '/' + '<int:uid>', methods=['DELETE'])
@auth.login_required()
def delete_user(uid):
    cur_auth_user = auth.current_user()

    if cur_auth_user[1] != 200:
        return cur_auth_user

    session = Session()
    deleter_status = session.query(User).filter_by(uid=cur_auth_user[0]).one().userstatus

    if deleter_status == 'admin':
        try:
            to_del = session.query(User).filter_by(uid=uid).one()
        except:
            return jsonify(USER_NOT_FOUND), 404
        to_del_status = to_del.userstatus
        if to_del_status == "admin" and uid != cur_auth_user[0]:
            return jsonify("Admin can`t delete another admin!"), 403
        else:
            session.delete(to_del)
            session.commit()
            return jsonify(USER_DELETED), 200
    elif cur_auth_user[0] != uid:
        return jsonify(ACCESS_DENIED + " [" + auth.username() + "] "), 403
    else:
        session = Session()
        try:
            user = session.query(User).filter_by(uid=uid).one()
        except:
            return jsonify(USER_NOT_FOUND), 404
        session.delete(user)
        session.commit()

    return jsonify(USER_DELETED), 200


# All about medicine
@app.route(BASE_PATH + MEDICINE_PATH, methods=['POST'])
@auth.login_required()
def place_medicine():
    current = auth.current_user()

    if current[1] != 200:
        return current

    if is_admin(User, current[0]):
        session = Session()
        medicine_request = request.get_json()
        try:
            try:
                if session.query(Medicine).filter_by(mid=medicine_request.get('mid')).one():
                    return jsonify(MEDICINE_ALREADY_EXIST), 400
            except:
                pass

            path_stat = medicine_request.get('status')
            if path_stat == 'available' or path_stat == 'pending' or path_stat == 'unavailable':
                medicine = Medicine(**medicine_request)
            else:
                return jsonify(INCORRECT_STATUS), 400

            session.add(medicine)
            session.commit()
            return jsonify(MEDICINE_PLACED), 201
        except:
            return jsonify(SOMETHING_WENT_WRONG), 400
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + MEDICINE_PATH + '/' + '<int:medicineId>', methods=['GET'])
def get_medicine_by_id(medicineId):
    session = Session()
    try:
        medicine = session.query(Medicine).filter_by(mid=medicineId).one()
    except:
        return jsonify(MEDICINE_NOT_FOUND), 404

    return jsonify(MedicineSchema().dump(medicine)), 200


@app.route(BASE_PATH + MEDICINE_PATH, methods=['GET'])
def get_all_medicines():
    session = Session()
    try:
        medicines = session.query(Medicine).all()
    except:
        medicines = []
    medicine_dto = MedicineSchema(many=True)
    return jsonify(medicine_dto.dump(medicines)), 200


@app.route(BASE_PATH + MEDICINE_PATH + '/' + '<int:medicineId>', methods=['DELETE'])
@auth.login_required()
def delete_medicine(medicineId):
    current = auth.current_user()

    if current[1] != 200:
        return current

    if is_admin(User, current[0]):
        session = Session()
        try:
            medicine = session.query(Medicine).filter_by(mid=medicineId).one()
        except:
            return jsonify(MEDICINE_NOT_FOUND), 404
        session.delete(medicine)
        session.commit()
        return jsonify(MEDICINE_DELETED), 200
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + MEDICINE_PATH + '/' + '<int:medicineId>', methods=['PUT'])
@auth.login_required()
def update_medicine(medicineId):
    current = auth.current_user()

    if current[1] != 200:
        return current

    if is_admin(User, current[0]):
        session = Session()
        try:
            if request.json['mid']:
                return jsonify(CANT_CHANGE_ID), 400
        except:
            pass
        try:
            update_request = request.get_json()

            try:
                medicine = session.query(Medicine).filter_by(mid=medicineId).one()
            except:
                return jsonify(MEDICINE_NOT_FOUND), 404

            update_medicine = update_util(medicine, update_request)

            if update_medicine == None:
                return jsonify(SOMETHING_WENT_WRONG), 400

            session.commit()
            return jsonify(MEDICINE_EDITED), 200
        except:
            return jsonify(SOMETHING_WENT_WRONG), 400
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + DEMAND_MEDICINE_PATH + '/' + '<int:medicineId>', methods=['PUT'])
@auth.login_required()
def update2_medicine(medicineId):
    current = auth.current_user()

    if current[1] != 200:
        return current

    session = Session()
    update_request_demand = request.get_json()
    # try:
    #     if update_request_demand.get('mid'):
    #         return jsonify(CANT_CHANGE_ID), 400
    # except:
    #     pass
    try:
        try:
            medicine = session.query(Medicine).filter_by(mid=medicineId).one()
        except:
            return jsonify(MEDICINE_NOT_FOUND), 404

        set_false = {"demand": False}
        set_true = {"demand": True}

        # message for user
        if MedicineSchema().dump(medicine).get('demand') == True and not is_admin(User, current[0]):
            return jsonify('This product is already on demand :) '), 200

        # message for superuser
        if MedicineSchema().dump(medicine).get('demand') == False and is_admin(User, current[0]):
            return jsonify('This product is already NOT on demand. Admin, you don`t need to do it '), 200

        if MedicineSchema().dump(medicine).get('demand') and is_admin(User, current[0]):
            medicine.demand = set_false['demand']

        elif MedicineSchema().dump(medicine).get('demand') == False \
                and not is_admin(User, current[0]):

            medicine.demand = set_true['demand']
        else:
            return jsonify(SOMETHING_WENT_WRONG), 400

        if update_medicine == None:
            return jsonify(SOMETHING_WENT_WRONG), 400

        session.commit()
        return jsonify(DEMAND_EDITED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


# All about pharmacy

@app.route(BASE_PATH + PHARMACY_ORDERS_PATH, methods=['POST'])
@auth.login_required()
def create_order():
    current = auth.current_user()

    if current[1] != 200:
        return current

    if not is_admin(User, current[0]):

        session = Session()
        order_request = request.get_json()

        try:
            if session.query(Order).filter_by(oid=order_request.get('oid')).one():
                return jsonify(ORDER_ALREADY_EXIST), 401
        except:
            pass

        if current[0] != order_request.get('userId'):
            return jsonify(ACCESS_DENIED), 403

        try:

            path_stat = order_request.get('status')
            if path_stat == order_statuses[0] or path_stat == order_statuses[1] or path_stat == order_statuses[2]:
                order = Order(**order_request)
            else:
                return jsonify(SOMETHING_WENT_WRONG), 400
            session.add(order)
            session.commit()

            return jsonify(ORDER_CREATED), 201
        except:
            return jsonify(SOMETHING_WENT_WRONG), 400
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + PHARMACY_ORDERS_MEDICINES_PATH, methods=['POST'])
@auth.login_required()
def create_order_medicine():
    current = auth.current_user()

    if current[1] != 200:
        return current

    if not is_admin(User, current[0]):

        try:
            order_request = request.get_json()

            session = Session()

            # user_id_to_check = session.query(Order).filter_by(oid=order_request.get('order_id')).one().userId
            user_id_to_check = uidFromOrder(Order, order_request.get('order_id'))

            if current[0] != user_id_to_check:
                return jsonify(ACCESS_DENIED), 403

            try:
                order = session.query(Order).filter_by(oid=order_request.get('order_id')).one()
            except:
                return jsonify(ORDER_NOT_FOUND), 404
            try:
                medicine = session.query(Medicine).filter_by(mid=order_request.get('medicine_id')).one()
            except:
                return jsonify(MEDICINE_NOT_FOUND), 404

            order.medicine.append(medicine)

            session.commit()

            return jsonify(MEDICINE_ADDED_TO_ORDER), 201
        except:
            return jsonify(SOMETHING_WENT_WRONG), 400
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + PHARMACY_ORDERS_MEDICINES_PATH + '/' + '<int:orderId>' + '/' + '<int:medicineId>',
           methods=['DELETE'])
@auth.login_required()
def delete_medicine_from_order(orderId, medicineId):
    current = auth.current_user()

    if current[1] != 200:
        return current

    session = Session()

    try:
        order = session.query(Order).filter_by(oid=orderId).one()
    except:
        return jsonify(ORDER_NOT_FOUND), 404

    try:
        medicine = session.query(Medicine).filter_by(mid=medicineId).one()
    except:
        return jsonify(MEDICINE_NOT_FOUND), 404

    try:
        session.query(OrdersMedicine).filter_by(order_id=orderId, medicine_id=medicineId).one()
    except:
        return jsonify('There is no such medicine in order!'), 404

    userId = uidFromOrder(Order, orderId)

    if is_admin(User, current[0]) or userId == current[0]:

        order.medicine.remove(medicine)
        session.commit()

        return jsonify(MEDICINE_DELETED_FROM_ORDER), 200

    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + PHARMACY_ORDERS_MEDICINES_PATH, methods=['GET'])
@auth.login_required()
def get_all_order_medicine():
    current = auth.current_user()

    if current[1] != 200:
        return current

    if is_admin(User, current[0]):

        session = Session()
        try:
            order = session.query(OrdersMedicine).all()
        except:
            order = []

        order_dto = OrdersMedicineSchema(many=True)

        return jsonify(order_dto.dump(order)), 200
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + PHARMACY_ORDERS_PATH, methods=['GET'])
@auth.login_required()
def get_all_order():
    current = auth.current_user()

    if current[1] != 200:
        return current

    if is_admin(User, current[0]):
        session = Session()
        try:
            order = session.query(Order).all()
        except:
            order = []
        order_dto = OrderSchema(many=True)
        return jsonify(order_dto.dump(order)), 200

    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + PHARMACY_ORDERS_PATH + '/' + '<string:status>', methods=['GET'])
@auth.login_required()
def get_order_by_status(status):
    current = auth.current_user()

    if current[1] != 200:
        return current

    if not is_admin(User, current[0]):

        session = Session()

        isStatusCorrect = False
        for ostatus in order_statuses:
            if ostatus == status:
                isStatusCorrect = True
                break

        if not isStatusCorrect:
            return jsonify('You have entered a wrong status!'), 404

        try:
            order = session.query(Order).filter_by(status=status, userId=current[0]).all()
        except:
            return jsonify(ORDER_NOT_FOUND), 404

        order_dto = OrderSchema(many=True)

        return jsonify(order_dto.dump(order)), 200
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + PHARMACY_ORDERS_PATH + '/' + '<int:orderId>', methods=['GET'])
@auth.login_required()
def get_order_by_id(orderId):
    current = auth.current_user()

    if current[1] != 200:
        return current

    session = Session()

    try:
        order = session.query(Order).filter_by(oid=orderId).one()
    except:
        return jsonify(ORDER_NOT_FOUND), 404

    userIdFromOrder = uidFromOrder(Order, orderId)

    if (userIdFromOrder == current[0] or is_admin(User, current[0])):

        return jsonify(OrderSchema().dump(order)), 200
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + PHARMACY_ORDERS_PATH + '/' + '<int:orderId>', methods=['DELETE'])
@auth.login_required()
def delete_order(orderId):
    current = auth.current_user()

    if current[1] != 200:
        return current

    if is_admin(User, current[0]) or current[0] == uidFromOrder(Order, orderId):
        session = Session()

        if session.query(OrdersMedicine).filter_by(order_id=orderId).all():
            return jsonify("Sorry, firstly, you must delete all medicines from your order!")

        try:
            order = session.query(Order).filter_by(oid=orderId).one()
        except:
            return jsonify(ORDER_NOT_FOUND), 404
        session.delete(order)
        session.commit()

        return jsonify(ORDER_DELETED), 200
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + MEDICINE_CATEGORY, methods=['POST'])
@auth.login_required()
def create_medicine_category():
    current = auth.current_user()

    if current[1] != 200:
        return current

    if is_admin(User, current[0]):

        session = Session()
        order_request = request.get_json()
        try:
            if session.query(Category).filter_by(cid=order_request.get('cid')).one():
                return jsonify('Such category id already exists!')
        except:
            pass
        try:
            if session.query(Category).filter_by(name=order_request.get('name')).one():
                return jsonify('Such category name already exists!')
        except:
            pass
        try:
            new_med_category = Category(**order_request)
            session.add(new_med_category)
            session.commit()
            return jsonify('Category`s been successfully created!'), 201
        except:
            return jsonify(SOMETHING_WENT_WRONG), 400
    else:
        return jsonify(ACCESS_DENIED), 403


@app.route(BASE_PATH + MEDICINE_CATEGORY + '/' + '<int:cid>', methods=['DELETE'])
@auth.login_required()
def delete_medicine_category(cid):
    current = auth.current_user()

    if current[1] != 200:
        return current

    if is_admin(User, current[0]):

        session = Session()
        try:
            to_delete = session.query(Category).filter_by(cid=cid).one()
        except:
            return jsonify('Category not found!'), 404
        try:
            session.delete(to_delete)
            session.commit()
            return jsonify('Category`s been successfully deleted!'), 200
        except:
            return jsonify(SOMETHING_WENT_WRONG), 400
    else:
        return jsonify(ACCESS_DENIED), 403


if __name__ == '__main__':
    app.run(debug=True)

# venv\Scripts\activate
# waitress-serve --host 127.0.0.1 --port=5000 --call "main:create_app"
# /api/v1/hello-world-15
# /api/v1/hello-world
# curl -v -XGET http://localhost:5000/api/v1/hello-world-15
