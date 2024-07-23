from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Connect VM with KV
keyVaultName = "vera-keys"
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)
password = client.get_secret("shein-password")

website = "https://sellerhub.shein.com/#/login"
username = "PCO017"
username_xpath = '//input[@name="username"]'
password_xpath = '//input[@name="password"]'
product_xpath = '//span[@title="商品"]'
productlist_xpath = '//span[@title="商品列表"]'
batch_menu_xpath =  '//span[text()="批量导出"]/ancestor::div[@class="so-select-inner so-select-drop-down"]'
batch_export_xpath =  "//a[.//span[text()='批量导出']]"
file_xpath = '(//table)[2]//tr[1]//td[3]//a'
userlabel_xpath = '//div[contains(@class, "shein-components_soc-fe-sso-sdk_user")]//div[contains(@class, "shein-components_soc-fe-sso-sdk_label")]'
logout_xpath = '//div[contains(@class, "shein-components_soc-fe-sso-sdk_logoutItem")]'

# Creating a new Chrome browser instance
s = Service(ChromeDriverManager().install())
chrome_options = Options()
user_data_dir = 'C:\\Users\\veraasadmin\\Documents\\python scripts\\selenium'
chrome_options.add_argument(f'user-data-dir={user_data_dir}')
driver = webdriver.Chrome(service=s, options=chrome_options)

# Navigate to the website's login page
driver.get(website)

# Find the username field, enter the username and click login
wait = WebDriverWait(driver, 5)

wait.until(EC.presence_of_element_located((By.XPATH, username_xpath))).send_keys(username)
wait.until(EC.presence_of_element_located((By.XPATH, password_xpath))).send_keys(password.value)
time.sleep(3)
login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.so-button.so-button-default.style__login_btn--nwCyS5Yt')))
login_button.click()

# time.sleep(30)
# handle the pop up window
try:
    button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.so-button.so-button-primary")))
    button.click()
    login_button.click()
except TimeoutException:
    # Handle the exception or pass to proceed to the next step if the element doesn't exist.
    pass

# from main page navigate to product list
time.sleep(3)

wait.until(EC.presence_of_element_located((By.XPATH, product_xpath))).click()
wait.until(EC.presence_of_element_located((By.XPATH, productlist_xpath))).click()

# batch export
time.sleep(5)
wait.until(EC.presence_of_element_located((By.XPATH, batch_menu_xpath))).click()

time.sleep(1)
wait.until(EC.presence_of_element_located((By.XPATH, batch_export_xpath))).click()

# switch to export window
# print(driver.window_handles)
time.sleep(30)
driver.switch_to.window(driver.window_handles[-1])
driver.refresh()
wait.until(EC.presence_of_element_located((By.XPATH, file_xpath))).click()

time.sleep(3)
driver.close()

# back to the first window and log out
driver.switch_to.window(driver.window_handles[0])
wait.until(EC.presence_of_element_located((By.XPATH, userlabel_xpath))).click()
wait.until(EC.presence_of_element_located((By.XPATH, logout_xpath))).click()
time.sleep(5)

driver.quit()
