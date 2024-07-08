from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Connect VM with KV
keyVaultName = "vera-keys"
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)
password = client.get_secret("mirakl-password")

website = "https://macysus-prod.mirakl.net/login"
username = "verahu@pconlineus.com"
username_id = "username"
submitbutton_id = 'submitButton'
password_id = 'password'
login_xpath = '//button[contains(text(), "Sign in")]'
catalog_id = 'catalog' 
catalog_manager_id = 'mcm-inventory' 
checkbox_xpath =  '//*[@id="pds-list-page"]/thead/tr/th[1]/div/label/div' 
select_all_xpath = '//button[span[contains(text(),"Select all products")]]'
export_button_id = 'ExportProductsButton'
download_export_xpath = '//button[span[text()="Download last generated export file"]]'
clear_xpath = '//button[span[text()="Clear selection"]]'
filter_id = 'metaStatus'
published_checkbox_xpath = '//*[@id="autocomplete-metaStatus-menu"]/div/div/div[5]'

# Creating a new Chrome browser instance
s = Service(ChromeDriverManager().install())
chrome_options = Options()
user_data_dir = 'C:\\Users\\veraasadmin\\Documents\\python scripts\\selenium'
chrome_options.add_argument(f'user-data-dir={user_data_dir}')
driver = webdriver.Chrome(service=s, options=chrome_options)

# Navigate to the website's login page
driver.get(website)

# Find the username field, enter the username and click login
driver.find_element(By.ID, username_id).send_keys(username)
driver.find_element(By.ID, submitbutton_id).click()

wait = WebDriverWait(driver, 8)

wait.until(EC.presence_of_element_located((By.ID, password_id))).send_keys(password.value)
wait.until(EC.element_to_be_clickable((By.XPATH, login_xpath))).click()

#time.sleep(100)

# product catalog
wait.until(EC.element_to_be_clickable((By.ID,catalog_id)))
driver.find_element(By.ID, catalog_id).click()

wait.until(EC.element_to_be_clickable((By.ID, catalog_manager_id)))
driver.find_element(By.ID, catalog_manager_id).click()

time.sleep(60)
# select all product
time.sleep(3)
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
driver.find_element(By.XPATH, checkbox_xpath).click()

all_product = wait.until(EC.element_to_be_clickable((By.XPATH, select_all_xpath)))
all_product.click()

export_button = wait.until(EC.element_to_be_clickable((By.ID, export_button_id)))
export_button.click()

time.sleep(10)
dowload_button = wait.until(EC.element_to_be_clickable((By.XPATH, download_export_xpath)))
dowload_button.click()

# select published product
clear_button = wait.until(EC.element_to_be_clickable((By.XPATH, clear_xpath)))
clear_button.click()

# filter by status
filter = wait.until(EC.element_to_be_clickable((By.ID, filter_id)))
filter.click()

published_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, published_checkbox_xpath)))
published_checkbox.click()

element = driver.find_element(By.CSS_SELECTOR, 'div.page-header')
element.click()
time.sleep(3)

# repeat download procedures
wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
driver.find_element(By.XPATH, checkbox_xpath).click()

all_product = wait.until(EC.element_to_be_clickable((By.XPATH, select_all_xpath)))
all_product.click()

export_button = wait.until(EC.element_to_be_clickable((By.ID, export_button_id)))
export_button.click()

time.sleep(10)
dowload_button = wait.until(EC.element_to_be_clickable((By.XPATH, download_export_xpath)))
dowload_button.click()
time.sleep(3)

driver.quit()
