import unittest
from flask import abort, url_for
from flask_testing import TestCase
from os import getenv
from application import app,db
from application.models import Users


class TestBase(TestCase):
     def create_app(self):
         config_name = 'testing'
         app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://'+str(getenv('MYSQL_USER'))+':'+str(getenv('MYSQL_PASS'))+'@'+str(getenv('MYSQL_URL'))+'/'+str(getenv('MYSQL_DB_TEST')))              
         return app
class Test(TestBase):
     def test_aboutpage_view(self):
        #Test that aboutpage is accesible
        response = self.client.get(url_for('about'))
        self.assertEqual(response.status_code, 200)
     def test_login_view(self):
        #Test that loginpage is accesible
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)
     def test_register_view(self):
        #Test that registerpage is accesible
        response = self.client.get(url_for('register'))
        self.assertEqual(response.status_code, 200)
    

