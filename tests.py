from unittest import TestCase
from flask.cli import locate_app

from config import TestingConfig
from app import db


class basictests(TestCase):
    def setUp(self):
        testApp = locate_app(TestingConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        # add_test_data_to_db()
    def tearDown(self):
        db.session.remove()
        db.drop.all()
        self.app_context.pop()
    def test_password_hashtag(self):
        s = student.query.get('1124555')
    


