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

driver.get('https://bursaacademy.bursamarketplace.com/en/login')

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl13_btnLogin"]'))  # Make sure submit button presence
)
print('login page: ', driver.title)
driver.find_element(By.XPATH, '//*[@id="ctl13_txtEmail"]').send_keys('xushengchin@gmail.com')
driver.find_element(By.XPATH, '//*[@id="ctl13_txtPassword"]').send_keys('5Qn5CLl#')
time.sleep(5)
driver.find_element(By.XPATH, '//*[@id="ctl13_btnLogin"]').click()
# driver.quit()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="newnav"]/div[2]/div[1]/div[1]/div[6]/div[1]/a'))
)
print('dashboard: ', driver.title)
# Click stimulator, open trading portal tab
driver.find_element(By.XPATH, '//*[@id="newnav"]/div[2]/div[1]/div[1]/div[6]/div[1]/a').click()
time.sleep(1)
driver.switch_to.window(driver.window_handles[0])  # Switch back to dashboard tab
time.sleep(1.5)
driver.close()  # Close dashboard tab
driver.switch_to.window(driver.window_handles[0])  # Switch to trading portal tab
time.sleep(3)
try:
    # Make sure trading portal is ready
    print('trading portal: ', driver.title)
    time.sleep(5)
    driver.refresh()
    print('done refresh')
    time.sleep(3)

    driver.switch_to.frame('tclitewin') # Switch to the targeted iframe

    element3 = driver.find_element(By.XPATH, '//*[@id="gridcolumn-1437-titleEl"]')
    print('e2=', element3)
    table = driver.find_element(By.XPATH, '//*[@id="gridview-1478"]/div[2]')
    print('table', table)

    # my_stock = value.setup_stock_list(driver)
    # print(my_stock)
    # driver.quit()
except Exception as e:
    print(e)
       # driver.quit()
    print('err')
