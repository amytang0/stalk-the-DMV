from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium import webdriver
from settings import PROFILE, URL
from logger import Logger
import time
from datetime import datetime

class Scraper:
    def __init__(self):
        self.logger = Logger()
        self.logger.log("New instance of scraper created")
        browser = webdriver.PhantomJS('phantomjs')
        # browser = webdriver.Chrome('./chromedriver')
        browser.get(URL)
        self.browser = browser
        self.logger.log("Navigated to url")
        time.sleep(5)

    def i_want_an_appointment_at(self, office_id):
        self.logger.log("Start appointment searching process")
        browser = self.form_fill_and_submit(self.browser, office_id)
        browser.switch_to_default_content()
        appt = self.get_appointment(browser)
        if appt == None:
            return None
        if appt and appt[:5] == 'Sorry':
            return None
        date_object = datetime.strptime(appt.strip(), "%A, %B %d, %Y at %I:%M %p")
        # This is the criteria you use to determine the date, feel free to change this
        if date_object == datetime(2018,10,20):
            self.confirm_appointment(browser)
        return appt

    def confirm_appointment(self, browser): 
        browser.find_element_by_xpath('//*[@id="app_content"]/div/a[1]').click()
        wait = WebDriverWait(browser, 200)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ApptForm"]/input')))
        browser.find_element_by_xpath('//*[@id="ApptForm"]/input').click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app_content"]/form/fieldset/div[11]/input')))
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/div[11]/input').click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ApptForm"]/fieldset/div[10]/input')))
        browser.find_element_by_xpath('//*[@id="ApptForm"]/fieldset/div[10]/input').click()

    def form_fill_and_submit(self, browser, office_id):
        browser.find_element_by_xpath('//*[@id="officeId"]/option[{}]'.format(office_id)).click()
        browser.find_element_by_xpath('//*[@id="one_task"]').click()
        browser.find_element_by_xpath('//*[@id="taskRID"]').click()
        browser.find_element_by_xpath('//*[@id="first_name"]').send_keys(PROFILE['first_name'])
        browser.find_element_by_xpath('//*[@id="last_name"]').send_keys(PROFILE['last_name'])
        browser.find_element_by_xpath('//*[@id="areaCode"]').send_keys(PROFILE['tel_prefix'])
        browser.find_element_by_xpath('//*[@id="telPrefix"]').send_keys(PROFILE['tel_suffix1'])
        browser.find_element_by_xpath('//*[@id="telSuffix"]').send_keys(PROFILE['tel_suffix2'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/div[8]/input[2]').click()
        self.logger.log("Form filled and submitted for office %s" % office_id)
        return browser

    def get_appointment(self, browser):
        time.sleep(5)
        try:
            element = browser.find_element_by_xpath('//*[@id="formId_1"]/div/div[2]/table/tbody/tr/td[3]/p[2]/strong').get_attribute('innerHTML')

            self.logger.log("Valid appointment xpath found")
            return element
        except:
            self.logger.log("No valid appointment xpath found")
            pass
        try:
            element = browser.find_element_by_xpath('//*[@id="app_content"]/table/tbody/tr[2]/td/p').get_attribute('innerHTML')
            self.logger.log("No available appointments")
            return element
        except:
            self.logger.log("Invalid xpath - no element found")
            pass
        return None
