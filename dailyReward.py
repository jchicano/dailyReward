import os
import sys
from sys import platform
import time
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')  # linux only
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
# options.headless = True  # also works

# if platform == "linux" or platform == "linux2":
#     browser = webdriver.Chrome('./webdriver/chromedriver-linux')
# elif platform == "darwin":
#     browser = webdriver.Chrome('./webdriver/chromedriver-mac')
# elif platform == "win32":
#     browser = webdriver.Chrome('./webdriver/chromedriver.exe')
# browser = webdriver.Chrome(
#     executable_path='./webdriver/chromedriver-mac', options=options)
browser = webdriver.Chrome(
    '/usr/lib/chromium-browser/chromedriver', options=options)  # rpi

browser.implicitly_wait(10)  # up to 10 seconds to find elements

load_dotenv()

USERNAME = os.getenv("DAILY_USER")
PASSWORD = os.getenv("DAILY_PASS")
URL = os.getenv("DAILY_URL")

is_phone_guard_method = input(
    'Are you using Steam Guard with your phone? (Y/n): ')
if is_phone_guard_method == 'Y' or is_phone_guard_method == 'y' or is_phone_guard_method == '':
    is_phone_guard_method = True
else:
    is_phone_guard_method = False

browser.get(URL)
browser.find_element_by_xpath('//*[@id="top-bar"]/div/a').click()
steam_login_url = browser.find_element_by_xpath(
    '//*[@id="loginForm"]/div/div[1]/div[3]/a').get_attribute("href")
browser.get(steam_login_url)
username_input = browser.find_element_by_xpath(
    '//*[@id="steamAccountName"]')
username_input.send_keys(USERNAME)
password_input = browser.find_element_by_xpath(
    '//*[@id="steamPassword"]')
password_input.send_keys(PASSWORD)
sign_in_button = browser.find_element_by_xpath(
    '//*[@id="imageLogin"]')
sign_in_button.click()

if is_phone_guard_method:
    print('*Preparing Phone Auth*')
    steam_guard_code = input('Enter your Steam Guard Code: ')
    steam_guard_code = steam_guard_code.upper()
    steam_guard_input = browser.find_element_by_xpath(
        '//*[@id="twofactorcode_entry"]')
    steam_guard_input.send_keys(steam_guard_code)
    steam_guard_submit = browser.find_element_by_xpath(
        '//*[@id="login_twofactorauth_buttonset_entercode"]/div[1]')
    steam_guard_submit.click()
    time.sleep(3)
else:
    print('*Preparing Mail Auth*')
    steam_guard_code = input('Enter your Steam Guard Code: ')
    steam_guard_code = steam_guard_code.upper()
    steam_guard_input = browser.find_element_by_xpath(
        '//*[@id="authcode"]')
    steam_guard_input.send_keys(steam_guard_code)
    steam_guard_submit = browser.find_element_by_xpath(
        '//*[@id="auth_buttonset_entercode"]/div[1]')
    steam_guard_submit.click()
    time.sleep(3)
    steam_guard_proceed_button = browser.find_element_by_xpath(
        '//*[@id="success_continue_btn"]')
    steam_guard_proceed_button.click()

print('*Login Completed*')

claimed_counter = 0
browser.implicitly_wait(0)

try:
    while True:  # claim daily reward
        browser.get(URL + '/rewards')
        # browser.find_element_by_xpath(
        #     '//*[@id="reward-claim-submit"]').click()
        try:
            if(browser.find_element_by_xpath('//*[@id="reward-claim-submit"]')):
                browser.find_element_by_xpath(
                    '//*[@id="reward-claim-submit"]').click()
                claimed_counter += 1
                print('**Claimed %d Time(s)**' % claimed_counter)
        except:
            # wait 10 minutes + random time
            t = 600 + random.randint(20, 30)
            print('*Waiting %d Seconds*' % t)
            time.sleep(t)
except KeyboardInterrupt:
    pass

print('\n\n****Claiming Finished****')
