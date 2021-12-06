from unittest import TestCase, main
from unittest.mock import ANY

import sqlalchemy

import authorization_methods
from app import app
from constants import *
from models import User, Category, Medicine, Order, OrdersMedicine, BaseModel, Session, engine
import schemas
import utils
import bcrypt
import json
from flask import url_for
from base64 import b64encode

app.testing = True
client = app.test_client()


class BaseTestCase(TestCase):
    client = app.test_client()

    def setUp(self):
        super().setUp()

        # Users and admins data
        self.admin_1_data = {
            "email": "admin1@gmail.com",
            "firstname": "Ivan",
            "lastname": "Petrenko",
            "password": "admin1",
            "phone": "0999309899",
            "username": "admin1",
            "userstatus": "admin"
        }

        self.admin_1_data_hashed = {
            **self.admin_1_data,
            "password": bcrypt.hashpw(bytes(self.admin_1_data['password'], 'utf-8'), bcrypt.gensalt())
        }

        self.admin_1_credentials = b64encode(b"admin1:admin1").decode('utf-8')

        self.admin_2_data = {
            "email": "admin2@gmail.com",
            "firstname": "Petro",
            "lastname": "Ivanenko",
            "password": "admin2",
            "phone": "0880009899",
            "username": "admin2",
            "userstatus": "admin"
        }

        self.admin_2_data_hashed = {
            **self.admin_2_data,
            "password": bcrypt.hashpw(bytes(self.admin_2_data['password'], 'utf-8'), bcrypt.gensalt())
        }

        self.admin_2_credentials = b64encode(b"admin2:admin2").decode('utf-8')

        self.user_1_data = {
            "uid": 1,
            "email": "user1@gmail.com",
            "firstname": "Vlad",
            "lastname": "Diachyk",
            "password": "user1",
            "phone": "0880777899",
            "username": "user1",
            "userstatus": "user"
        }

        self.user_1_data_hashed = {
            **self.user_1_data,
            "password": bcrypt.hashpw(bytes(self.user_1_data['password'], 'utf-8'), bcrypt.gensalt())
        }

        self.user_1_credentials = b64encode(b"user1:user1").decode('utf-8')

        self.user_2_data = {
            "uid": 2,
            "email": "user2@gmail.com",
            "firstname": "Bob",
            "lastname": "Marlin",
            "password": "user2",
            "phone": "0980722899",
            "username": "user2",
            "userstatus": "user"
        }

        self.user_2_data_hashed = {
            **self.user_2_data,
            "password": bcrypt.hashpw(bytes(self.user_2_data['password'], 'utf-8'), bcrypt.gensalt())
        }

        self.user_2_credentials = b64encode(b"user2:user2").decode('utf-8')

        # Category data
        self.category_1_data = {
            "cid": 1,
            "name": "Spray"
        }

        self.category_2_data = {
            "cid": 2,
            "name": "Pills"
        }

        # Medicines data
        self.medicine_1_data = {
            "mid": 1,
            "category": 2,
            "demand": False,
            "manufacturer": "HeartBeat",
            "name": "Cardiomagnil",
            "status": "available"
        }

        self.medicine_2_data = {
            "category": 1,
            "demand": False,
            "manufacturer": "Farmak",
            "name": "Pshyk",
            "status": "available"
        }

        # Orders data
        self.order_1_data = {
            "oid": 1,
            "shipDate": "2019-05-08T17:12:05",
            "status": "placed",
            "userId": 1
        }

        self.order_2_data = {
            "oid": 2,
            "shipDate": "2020-05-08T17:12:05",
            "status": "placed",
            "userId": 2
        }

        # Orders-Medicines data
        self.order_medicine_1_data = {
            "order_id": 1,
            "medicine_id": 1
        }

        self.order_medicine_2_data = {
            "order_id": 2,
            "medicine_id": 2
        }

    def tearDown(self):
        self.close_session()

    def close_session(self):
        Session.close()

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def get_auth_headers(self, credentials):
        return {"Authorization": f"Basic {credentials}"}

    # Methods for the database
    def clear_user_db(self):
        engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from user;')

    def clear_category_db(self):
        engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from category;')

    def clear_medicine_db(self):
        engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from medicine;')

    def clear_order_db(self):
        engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from orders;')

    def clear_order_medicine_db(self):
        engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from orders_medicine;')

    def create_all_users(self):
        self.client.post('api/v15/user', json=self.user_1_data)
        self.client.post('api/v15/user', json=self.user_2_data)
        self.client.post('api/v15/user', json=self.admin_1_data)
        self.client.post('api/v15/user', json=self.admin_2_data)

    def create_all_categories(self):
        self.client.post('api/v15/medicine/category', json=self.category_1_data,
                         headers=self.get_auth_headers(self.admin_1_credentials))
        self.client.post('api/v15/medicine/category', json=self.category_2_data,
                         headers=self.get_auth_headers(self.admin_1_credentials))

    def create_all_medicines(self):
        self.client.post('api/v15/medicine', json=self.medicine_1_data,
                         headers=self.get_auth_headers(self.admin_1_credentials))
        self.client.post('api/v15/medicine', json=self.medicine_2_data,
                         headers=self.get_auth_headers(self.admin_1_credentials))

    def create_all_orders(self):
        self.client.post('api/v15/pharmacy/orders', json=self.order_1_data,
                         headers=self.get_auth_headers(self.user_1_credentials))
        self.client.post('api/v15/pharmacy/orders', json=self.order_2_data,
                         headers=self.get_auth_headers(self.user_2_credentials))

    def create_all_order_medicine_tables(self):
        self.client.post('api/v15/pharmacy/orders/medicines', json=self.order_medicine_1_data,
                         headers=self.get_auth_headers(self.user_1_credentials))

        self.client.post('api/v15/pharmacy/orders/medicines', json=self.order_medicine_2_data,
                         headers=self.get_auth_headers(self.user_2_credentials))


class TestUser(BaseTestCase):
    def test_create_user_1(self):
        self.clear_user_db()
        response = self.client.post('api/v15/user', json=self.user_1_data)
        self.assertEqual(response.status_code, 201)

    def test_create_not_unique_user(self):
        self.clear_user_db()
        self.client.post('api/v15/user', json=self.user_1_data)
        response = self.client.post('api/v15/user', json=self.user_1_data)
        self.assertEqual(response.status_code, 409)

    def test_get_all_users(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.get('api/v15/user', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_all_users_not_admin(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.get('api/v15/user', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_get_user_by_id(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.get('api/v15/user/1', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_not_existing_id(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.get('api/v15/user/-1', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_get_user_by_id_access_denied(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.get('api/v15/user/1', headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_update_user(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.put('api/v15/user/2', data=json.dumps({
            "email": "new@gmail.com",
            "firstname": "Vladww",
            "lastname": "Diachykww",
            "password": "userwww",
            "phone": "02777899",
            "username": "user22"
        }),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 200)

    def test_update_user_id(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.put('api/v15/user/1', data=json.dumps({"uid": 10}),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_update_user_access_denied(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.put('api/v15/user/1', data=json.dumps({"email": "yura90@gmail.com"}),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_delete_user(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.delete('api/v15/user/1', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_user_access_denied(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.delete('api/v15/user/1', headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_delete_not_existing_user(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.delete('api/v15/user/-1', headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 404)


class TestCategory(BaseTestCase):
    def test_create_category(self):
        self.clear_category_db()
        response = self.client.post('api/v15/medicine/category', json=self.category_1_data,
                                    headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 201)

    def test_create_category_access_denied(self):
        self.clear_category_db()
        response = self.client.post('api/v15/medicine/category', json=self.category_1_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_delete_category(self):
        self.clear_category_db()
        self.create_all_categories()

        response = self.client.delete('api/v15/medicine/category/1',
                                      headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_category_access_denied(self):
        self.clear_category_db()
        self.create_all_categories()

        response = self.client.delete('api/v15/medicine/category/1',
                                      headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_delete_not_existing_category(self):
        self.clear_category_db()
        self.create_all_categories()

        response = self.client.delete('api/v15/medicine/category/-1',
                                      headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)


class TestMedicine(BaseTestCase):
    def test_create_medicine(self):
        self.clear_medicine_db()
        response = self.client.post('api/v15/medicine', json=self.medicine_1_data,
                                    headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 201)

    def test_create_not_unique_medicine(self):
        self.clear_medicine_db()
        self.client.post('api/v15/medicine', json=self.medicine_1_data,
                         headers=self.get_auth_headers(self.admin_1_credentials))
        response = self.client.post('api/v15/medicine', json=self.medicine_1_data,
                                    headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_create_medicine_access_denied(self):
        self.clear_medicine_db()
        response = self.client.post('api/v15/medicine', json=self.medicine_1_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_get_all_medicines(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.get('api/v15/medicine')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {
                "mid": 1,
                "category": 2,
                "demand": False,
                "manufacturer": "HeartBeat",
                "name": "Cardiomagnil",
                "status": "available"
            },
            {
                "mid": ANY,
                "category": 1,
                "demand": False,
                "manufacturer": "Farmak",
                "name": "Pshyk",
                "status": "available"
            }
        ])

    def test_get_medicine_by_id(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.get('api/v15/medicine/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {
                             "mid": 1,
                             "category": 2,
                             "demand": False,
                             "manufacturer": "HeartBeat",
                             "name": "Cardiomagnil",
                             "status": "available"
                         }
                         )

    def test_get_not_existing_medicine_by_id(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.get('api/v15/medicine/-1')
        self.assertEqual(response.status_code, 404)

    def test_delete_medicine(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.delete('api/v15/medicine/1', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_not_existing_medicine(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.delete('api/v15/medicine/-1', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_delete_medicine_access_denied(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.delete('api/v15/medicine/1', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_update_medicine(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.put('api/v15/medicine/1', data=json.dumps({
            "category": 1,
            "manufacturer": "HeartBeat222",
            "name": "Cardiomagnil22",
            "status": "available22"
        }),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_update_medicine_id(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.put('api/v15/medicine/1', data=json.dumps({"mid": 100}),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_update_not_existing_medicine(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.put('api/v15/medicine/-1', data=json.dumps({"manufacturer": "Phaizer"}),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_update_medicine_access_denied(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.put('api/v15/medicine/1', data=json.dumps({"manufacturer": "Phaizer"}),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_add_medicine_to_demand(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.put('api/v15/demand/medicine/1', data=json.dumps({}),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_add_not_existing_medicine_to_demand(self):
        self.clear_medicine_db()
        self.create_all_medicines()

        response = self.client.put('api/v15/demand/medicine/-1', data=json.dumps({}),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 404)


class TestOrder(BaseTestCase):
    def test_create_order(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()

        response = self.client.post('api/v15/pharmacy/orders', json=self.order_1_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 201)

    def test_create_not_unique_order(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.post('api/v15/pharmacy/orders', json=self.order_1_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 401)

    def test_create_order_access_denied(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()

        response = self.client.post('api/v15/pharmacy/orders', json=self.order_1_data,
                                    headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_get_all_orders(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.get('api/v15/pharmacy/orders', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_all_orders_access_denied(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.get('api/v15/pharmacy/orders', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_get_order_by_status(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.get('api/v15/pharmacy/orders/placed',
                                   headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {
                "oid": 1,
                "shipDate": "2019-05-08T17:12:05",
                "status": "placed",
                "userId": 1
            }]
                         )

    def test_get_order_by_not_existing_status(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.get('api/v15/pharmacy/orders/asaca',
                                   headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_get_order_by_status_access_denied(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.get('api/v15/pharmacy/orders/placed',
                                   headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_get_order_by_id(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.get('api/v15/pharmacy/orders/1', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_not_existing_order_by_id(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.get('api/v15/pharmacy/orders/-1', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_get_order_by_id_access_denied(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.get('api/v15/pharmacy/orders/1', headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_delete_order(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.delete('api/v15/pharmacy/orders/1',
                                      headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_not_existing_order(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.delete('api/v15/pharmacy/orders/-1',
                                      headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 405)

    def test_delete_order_access_denied(self):
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.delete('api/v15/pharmacy/orders/1',
                                      headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_add_medicine_to_order(self):
        self.clear_order_medicine_db()
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.post('api/v15/pharmacy/orders/medicines', json=self.order_medicine_1_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 201)

    def test_add_medicine_to_order_access_denied(self):
        self.clear_order_medicine_db()
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.post('api/v15/pharmacy/orders/medicines', json=self.order_medicine_1_data,
                                    headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_add_medicine_to_not_existing_order(self):
        self.clear_order_medicine_db()
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()

        response = self.client.post('api/v15/pharmacy/orders/medicines', json={
            "order_id": -1,
            "medicine_id": 1
        },
                                    headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 400)

    def test_delete_medicine_from_order(self):
        self.clear_order_medicine_db()
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()

        response = self.client.delete('api/v15/pharmacy/orders/medicines/1/1',
                                      headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_medicine_from_order_access_denied(self):
        self.clear_order_medicine_db()
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()

        response = self.client.delete('api/v15/pharmacy/orders/medicines/1/1',
                                      headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_delete_medicine_from_not_existing_order(self):
        self.clear_order_medicine_db()
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()

        response = self.client.delete('api/v15/pharmacy/orders/medicines/-1/1',
                                      headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_delete_not_existing_medicine_from_order(self):
        self.clear_order_medicine_db()
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()

        response = self.client.delete('api/v15/pharmacy/orders/medicines/1/-1',
                                      headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_get_all_orders_medicines(self):
        self.clear_order_medicine_db()
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()

        response = self.client.get('api/v15/pharmacy/orders/medicines',
                                   headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_all_orders_medicines_access_denied(self):
        self.clear_order_medicine_db()
        self.clear_order_db()
        self.clear_user_db()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()

        response = self.client.get('api/v15/pharmacy/orders/medicines',
                                   headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)


class TestAuth(BaseTestCase):
    def test_get_user_by_id_with_wrong_username(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.get('api/v15/user/1',
                                   headers=self.get_auth_headers(b64encode(b"adwqddqw:admin1").decode('utf-8')))
        self.assertEqual(response.status_code, 401)

    def test_get_user_by_id_with_wrong_password(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.get('api/v15/user/1',
                                   headers=self.get_auth_headers(b64encode(b"admin1:adcqwcqc").decode('utf-8')))
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    main()
