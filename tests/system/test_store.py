from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                res = client.post('/store/test')

                self.assertEqual(res.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, res.get_json())

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                res = client.post('/store/test')

                self.assertEqual(res.status_code, 400)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                res = client.delete('/store/test')

                self.assertEqual(res.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'}, res.get_json())

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                res = client.get('/store/test')

                self.assertEqual(res.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, res.get_json())

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                res = client.get('/store/test')

                self.assertEqual(res.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, res.get_json())

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                res = client.get('/store/test')

                self.assertEqual(res.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]}, res.get_json())

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                res = client.get('/stores')

                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': []}]}, res.get_json())

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                res = client.get('/stores')

                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]}]},
                                     res.get_json())
