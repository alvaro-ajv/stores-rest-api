import json

from models.item import ItemModel
from models.user import UserModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})

                auth_token = auth_request.get_json()['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                res = client.get('/item/test')
                self.assertEqual(res.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                res = client.get('item/test', headers={'Authorization': self.access_token})
                self.assertEqual(res.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                res = client.get('item/test', headers={'Authorization': self.access_token})
                self.assertEqual(res.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                res = client.delete('item/test')
                self.assertEqual(res.status_code, 200)

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                res = client.post('/item/test', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(res.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, res.get_json())

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                client.post('/item/test', data={'price': 17.99, 'store_id': 1})
                res = client.post('/item/test', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(res.status_code, 400)
                self.assertDictEqual({'message': 'An item with name \'test\' already exists.'}, res.get_json())

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                res = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(res.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, res.get_json())

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                res = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(res.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, res.get_json())

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                res = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 5.99}]}, res.get_json())

