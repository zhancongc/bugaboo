import unittest
from flask import url_for
from app.views import index
from app import create_app, db
from app.models import User


class ViewTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def test_index(self):
        res = self.client.get(url_for('app.index'))
        self.assertEqual("Hello, World!", res.get_data(as_text=True), msg="index failed")
        print("check index")


if __name__ == "__main__":
    unittest.main()
