from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time


class MySeleniumTests(LiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_search_clickfirst(self):
        self.selenium.get(self.live_server_url)
        search_input = self.selenium.find_element_by_xpath(
            '/html/body/div[4]/form/div/div[2]/input')
        search_input.send_keys('network')
        self.selenium.find_element_by_xpath(
            '/html/body/div[4]/form/div[2]/div[2]/button').click()
        time.sleep(1)
        self.selenium.find_element_by_xpath(
            '/html/body/div[5]/div/div[2]/div/table/tbody/tr/td[2]/a'
            ).click()  # book
        time.sleep(1)
        self.selenium.find_element_by_xpath(
            '/html/body/div[5]/div/div/button').click()  # findbug
        time.sleep(0.2)
        author_input = self.selenium.find_element_by_xpath(
            '/html/body/div[10]/div/div/div[2]/form/div/div/input')
        author_input.send_keys('')
        self.selenium.find_element_by_xpath(
            '//*[@id="fixbookinfo-submit"]').click()  # change
        self.selenium.find_element_by_xpath(
            '/html/body/div[10]/div/div/div[3]/button').click()  # close
        time.sleep(1)
        self.selenium.find_element_by_xpath(
            '/html/body/div[8]/div/div/button').click()  # commant
        time.sleep(0.2)
        self.selenium.find_element_by_xpath(
            '//*[@id="makemycomment-submit"]').click()  # submit
        self.selenium.find_element_by_xpath(
            '//*[@id="isSpoiler"]').click()  # jutou
        title_input = self.selenium.find_element_by_xpath(
            '//*[@id="input-comment-title"]')
        username_input.send_keys('AoWu')
        self.selenium.find_element_by_xpath(
            '//*[@id="makemycomment-submit"]').click()  # submit
        self.selenium.find_element_by_xpath(
            '/html/body/div[9]/div/div/div[3]/button').click()  # close
