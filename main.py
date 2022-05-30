from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from read_email import get_code_from_mail, get_code_from_sms
from dotenv import load_dotenv
import os

load_dotenv()
TINDER_PHONE = os.getenv("my_phone")
TINDER_EMAIL = os.getenv("my_email")
TINDER_PASSWORD = os.getenv("tinder_password")
TINDER_URL = "https://tinder.com/"

chrome_driver_path = os.getenv("driver_location")
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

driver.get(TINDER_URL)
time.sleep(2)

try:
    driver.find_element(by=By.CSS_SELECTOR, value='[data-testid="privacyPreferencesAccept"]').click()
except NoSuchElementException:
    pass

time.sleep(1)
driver.find_element(by=By.CSS_SELECTOR, value='[data-testid="appLoginBtn"]').click()
time.sleep(3)

driver.find_element(by=By.XPATH,
                    value='//*[@id="o-1442994379"]/div/div/div[1]/div/div/div[3]/span/div[3]/button/span[2]').click()

while True:
    time.sleep(4)
    try:
        driver.find_element(by=By.XPATH,
                            value='//*[@id="o-1442994379"]/div/div/div[1]/div/div[2]/div/input').send_keys(TINDER_PHONE)
        break
    except NoSuchElementException:
        pass

driver.find_element(by=By.CSS_SELECTOR, value='[data-testid="phoneNumberInputSubmit"]').click()
time.sleep(2)

sms_code = get_code_from_sms()
print(sms_code)
for letter_index in range(0, 6):
    driver.find_element(by=By.XPATH,
                        value=f'//*[@id="o-1442994379"]/div/div/div[1]/div/div[2]/input[{letter_index + 1}]')\
        .send_keys(sms_code[letter_index])

driver.find_element(by=By.CSS_SELECTOR, value=f'[data-testid="SMSCodeInputSubmit"]').click()

time.sleep(2)
driver.find_element(by=By.XPATH, value='//*[@id="o-1442994379"]/div/div/div[1]/div/div[2]/button').click()

email_code = get_code_from_mail()
for letter_index in range(0, 6):
    driver.find_element(by=By.XPATH,
                        value=f'//*[@id="o-1442994379"]/div/div/div[1]/div/div[4]/input[{letter_index + 1}]')\
        .send_keys(email_code[letter_index])

driver.find_element(by=By.XPATH, value='//*[@id="o-1442994379"]/div/div/div[1]/div/button').click()

time.sleep(1)
driver.find_element(by=By.XPATH, value='//*[@id="o-1442994379"]/div/div/div/div/div[3]/button[1]').click()
driver.find_element(by=By.XPATH, value='//*[@id="o-1442994379"]/div/div/div/div/div[3]/button[2]/span').click()

for letter_index in range(0, 50):
    while True:
        time.sleep(0.5)
        try:
            driver.find_element(by=By.ID, value="Tinder").send_keys(Keys.ARROW_RIGHT)
            break
        except NoSuchElementException:
            pass
    time.sleep(0.5)
    try:
        driver.find_element(by=By.ID, value="Tinder").send_keys(Keys.ESCAPE)
    except NoSuchElementException:
        pass
