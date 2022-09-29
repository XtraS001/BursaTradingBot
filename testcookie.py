# Navigation to trading portal

# import module
# import value
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import value



# Create object
# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome(PATH)
driver = uc.Chrome()
driver.maximize_window()
driver.get("https://bursaacademy.bursamarketplace.com/en/login")

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    cookie['domain'] = '.bursamarketplace.com'
    try:
        driver.add_cookie(cookie)
    except Exception as e:
        print(e)

driver.get("https://bursaacademy.bursamarketplace.com/en/mydashboard")

time.sleep(3)