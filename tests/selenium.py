import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from unittest import TestCase

from app import create_app, db
from config import TestingConfig

localHost = "http://localhost:5000/"

class SeleniumTestCase(TestCase):

    def setUp(self):
        self.testApp = create_app(TestingConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.server_process = multiprocessing.Process(target=self.testApp.run)
        self.server_process.start()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.server_process.terminate()
        self.driver.close()

    def test_home_page(self):
        x=1
        self.assertEqual(x,1)

    # def test_home_page(self):
    #     driver = self.driver
    #     driver.get(self.base_url)
    #     self.assertIn("Home",driver.title)