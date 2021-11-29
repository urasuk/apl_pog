from flask import Flask, request, jsonify
from models import Session, User
from constants import *
from schemas import *
from utils import *
import bcrypt

app = Flask(__name__)


@app.route("/api/v15/hello-world-15")
def hello_world():
    return "<p>Hello World 15</p>"


@app.route("/api/v15/hello-world")
def hello_world2():
    return "<p>Hello World</p>"
# All about user
@app.route(BASE_PATH + USER_PATH, methods=['POST'])
def create_user():
    session = Session()
    try:
        user_request = request.get_json()

        user = User(**user_request)


        session.add(user)
        session.commit()

        return jsonify(USER_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + USER_PATH + '/' + '<int:Id>', methods=['GET'])
def get_user_by_userName(Id):
    session = Session()
    try:
        user = session.query(User).filter_by(uid=Id).one()
    except:
        return jsonify(USER_NOT_FOUND), 404

    return jsonify(UserSchema().dump(user)), 200


@app.route(BASE_PATH + USER_PATH, methods=['GET'])
def get_all_users():
    session = Session()
    try:
        users = session.query(User).all()
    except:
        users = []

    users_dto = UserSchema(many=True)

    return jsonify(users_dto.dump(users)), 200


@app.route(BASE_PATH + USER_PATH + '/' + '<int:Id>', methods=['PUT'])
def update_user(Id):
    session = Session()
    try:
        if request.json['Id']:
            return jsonify(CANT_CHANGE_ID), 400
    except:
        pass
    try:
        update_request = request.get_json()

        try:
            user = session.query(User).filter_by(uid=Id).one()
        except:
            return jsonify(USER_NOT_FOUND), 404

        update_user = update_util(user, update_request)

        if update_user == None:
            return jsonify(SOMETHING_WENT_WRONG), 400
        session.commit()
        return jsonify(USER_UPDATED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + USER_PATH + '/' + '<int:Id>', methods=['DELETE'])
def delete_user(Id):
    session = Session()
    try:
        user = session.query(User).filter_by(uid=Id).one()
    except:
        return jsonify(USER_NOT_FOUND), 404
    session.delete(user)
    session.commit()

    return jsonify(USER_DELETED), 200

# All about medicine
@app.route(BASE_PATH + MEDICINE_PATH, methods=['POST'])
def place_medicine():
    session = Session()
    try:
        medicine_request = request.get_json()
        path_stat = medicine_request.get('status')
        if path_stat == 'available' or path_stat == 'pending' or path_stat == 'unavailable':
            medicine = Medicine(**medicine_request)
        else:
            return jsonify(SOMETHING_WENT_WRONG), 400

        session.add(medicine)
        session.commit()

        return jsonify(MEDICINE_PLACED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


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
def delete_medicine(medicineId):
    session = Session()
    try:
        medicine = session.query(Medicine).filter_by(mid=medicineId).one()
    except:
        return jsonify(MEDICINE_NOT_FOUND), 404
    session.delete(medicine)
    session.commit()

    return jsonify(MEDICINE_DELETED), 200


@app.route(BASE_PATH + MEDICINE_PATH + '/' + '<int:medicineId>', methods=['PUT'])
def update_medicine(medicineId):
    session = Session()
    try:
        if request.json['medicineId']:
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

@app.route(BASE_PATH + DEMAND_MEDICINE_PATH + '/' + '<int:medicineId>', methods=['PUT'])
def update2_medicine(medicineId):
    session = Session()
    try:
        if request.json['medicineId']:
            return jsonify(CANT_CHANGE_ID), 400
    except:
        pass
    try:
        update_request_demand = request.get_json()

        try:
            medicine = session.query(Medicine).filter_by(mid=medicineId).one()
        except:
            return jsonify(MEDICINE_NOT_FOUND), 404

        #update_medicine = update_util(medicine, update_request_demand)
        #dem_dict = MedicineSchema().load(update_request_demand)

        update_request_demand_false = {"demand":False}
        update_request_demand_true = {"demand":True}

        if MedicineSchema().dump(medicine).get('demand'):
            medicine.demand = update_request_demand_false['demand']
            #update_util(medicine, update_request_demand_false)
        elif MedicineSchema().dump(medicine).get('demand') == False:
            #update_util(medicine, update_request_demand_true)
            medicine.demand = update_request_demand_true['demand']
        else:
            return jsonify(SOMETHING_WENT_WRONG), 400

        if update_medicine == None:
            return jsonify(SOMETHING_WENT_WRONG), 400


        session.commit()
        return jsonify(MEDICINE_EDITED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400

# All about pharmacy
@app.route(BASE_PATH + PHARMACY_ORDERS_PATH, methods=['POST'])
def create_order():
    session = Session()
    try:
        order_request = request.get_json()
        path_stat = order_request.get('status')
        if path_stat == 'placed' or path_stat == 'approved' or path_stat == 'delivered':
            order = Order(**order_request)
        else:
            return jsonify(SOMETHING_WENT_WRONG), 400
        session.add(order)
        session.commit()

        return jsonify(ORDER_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + PHARMACY_ORDERS_MEDICINES_PATH, methods=['POST'])
def create_order_medicine():
    session = Session()
    try:
        order_request = request.get_json()
        session = Session()
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

        return jsonify(ORDER_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + PHARMACY_ORDERS_MEDICINES_PATH + '/' + '<int:orderId>' + '/' + '<int:medicineId>', methods=['DELETE'])
def delete_medicine_from_order(orderId,medicineId):
    session = Session()
    try:
        order = session.query(Order).filter_by(oid=orderId).one()
    except:
        return jsonify(ORDER_NOT_FOUND), 404
    try:
        medicine = session.query(Medicine).filter_by(mid=medicineId).one()
    except:
        return jsonify(MEDICINE_NOT_FOUND), 404
    #spec_medicine = session.query(OrdersMedicine).filter_by(order_id='orderId',medicine_id='medicineId').one()
    #session.delete(spec_medicine)
    order.medicine.remove(medicine)
    session.commit()

    return jsonify(ORDER_DELETED), 200

@app.route(BASE_PATH + PHARMACY_ORDERS_MEDICINES_PATH, methods=['GET'])
def get_all_order_medicine():
    session = Session()
    try:
        order = session.query(OrdersMedicine).all()
    except:
        order = []

    order_dto = OrdersMedicineSchema(many=True)

    return jsonify(order_dto.dump(order)), 200


@app.route(BASE_PATH + PHARMACY_ORDERS_PATH, methods=['GET'])
def get_all_order():
    session = Session()
    try:
        order = session.query(Order).all()
    except:
        order = []

    order_dto = OrderSchema(many=True)

    return jsonify(order_dto.dump(order)), 200


@app.route(BASE_PATH + PHARMACY_ORDERS_PATH + '/' + '<string:status>', methods=['GET'])
def get_order_by_status(status):
    session = Session()
    try:
        order = session.query(Order).filter_by(status=status).all()
    except:
        return jsonify(ORDER_NOT_FOUND), 404

    order_dto = OrderSchema(many=True)

    return jsonify(order_dto.dump(order)), 200


@app.route(BASE_PATH + PHARMACY_ORDERS_PATH + '/' + '<int:orderId>', methods=['GET'])
def get_order_by_id(orderId):
    session = Session()
    try:
        order = session.query(Order).filter_by(oid=orderId).one()
    except:
        return jsonify(ORDER_NOT_FOUND), 404

    return jsonify(OrderSchema().dump(order)), 200


@app.route(BASE_PATH + PHARMACY_ORDERS_PATH + '/' + '<int:orderId>', methods=['DELETE'])
def delete_order(orderId):
    session = Session()
    try:
        order = session.query(Order).filter_by(oid=orderId).one()
    except:
        return jsonify(ORDER_NOT_FOUND), 404
    session.delete(order)
    session.commit()

    return jsonify(ORDER_DELETED), 200

if __name__ == '__main__':
    app.run(debug=True)
# venv\Scripts\activate
# waitress-serve --host 127.0.0.1 --port=5000 --call "main:create_app"
# /api/v1/hello-world-15
# /api/v1/hello-world

# curl -v -XGET http://localhost:5000/api/v1/hello-world-15