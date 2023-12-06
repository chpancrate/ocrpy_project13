import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

TIME_SLEEP = 0


class OCLettingsSite(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_profiles_path(self):
        # connect to homepage
        self.driver.get('http://localhost:8000/')
        time.sleep(TIME_SLEEP)

        # check homepage displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Welcome to Holiday Homes')

        # click on profiles button
        profiles_button = self.driver.find_element(By.LINK_TEXT, "Profiles")
        profiles_button.click()
        time.sleep(TIME_SLEEP)

        # check profiles page displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Profiles')

        # click on an item in list
        item = self.driver.find_element(By.LINK_TEXT, "HeadlinesGazer")
        item.click()
        time.sleep(TIME_SLEEP)

        # check details page displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'HeadlinesGazer')

        # click on back button
        item = self.driver.find_element(By.LINK_TEXT, "Back")
        item.click()
        time.sleep(TIME_SLEEP)

        # check profiles page displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Profiles')

    def test_lettings_path(self):
        # connect to homepage
        self.driver.get('http://localhost:8000/')
        time.sleep(TIME_SLEEP)

        # check homepage displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Welcome to Holiday Homes')

        # click on lettings button
        profiles_button = self.driver.find_element(By.LINK_TEXT, "Lettings")
        profiles_button.click()
        time.sleep(TIME_SLEEP)

        # check lettings page displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Lettings')

        # click on an item in list
        item = self.driver.find_element(By.LINK_TEXT, "Oceanview Retreat")
        item.click()
        time.sleep(TIME_SLEEP)

        # check details page displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Oceanview Retreat')

        # click on back button
        item = self.driver.find_element(By.LINK_TEXT, "Back")
        item.click()
        time.sleep(TIME_SLEEP)

        # check lettings page displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Lettings')

    def test_page_404(self):
        # connect to homepage
        self.driver.get('http://localhost:8000/')
        time.sleep(TIME_SLEEP)

        # check homepage displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Welcome to Holiday Homes')

        # go to wrong url
        self.driver.get('http://localhost:8000/wrgurl')
        time.sleep(TIME_SLEEP)

        # check 404 page displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Page not found')

    def test_page_500(self):
        # connect to homepage
        self.driver.get('http://localhost:8000/')
        time.sleep(TIME_SLEEP)

        # check homepage displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Welcome to Holiday Homes')

        # go to wrong url
        self.driver.get('http://localhost:8000/lettings/999/')
        time.sleep(TIME_SLEEP)

        # check 404 page displayed
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text,
                         'Internal Error')
