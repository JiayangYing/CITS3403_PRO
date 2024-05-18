import multiprocessing
import threading
from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import unittest

from app import create_app, db
from config import TestingConfig

localHost = "http://localhost:5000/"

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        try:
            # cls.client = webdriver.Firefox()
            cls.client = webdriver.Chrome()
        except:
            pass
        if cls.client:
            cls.testApp = create_app(TestingConfig)
            cls.app_context = cls.testApp.app_context()
            cls.app_context.push()
            db.create_all()

            threading.Thread(target=cls.app.run).start()
            time.sleep(1)
            
            cls.server_process = multiprocessing.Process(target=cls.testApp.run)
            cls.server_process.start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop the flask server and the browser
            cls.client.get(localHost)
            cls.client.close()
            db.drop_all()
            db.session.remove()
            cls.app_context.pop()
            cls.server_process.terminate()
            # cls.driver.close()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_home_page(self):
        driver = self.driver
        driver.get(self.base_url)
        self.assertIn("Home",driver.title)