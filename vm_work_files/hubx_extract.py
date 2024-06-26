from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
password = client.get_secret("hubx-password")

website = "https://hubx.com/vendor-login"
username = "b2b@pconline365.com"
login_xpath = '//a[span="Vendor Login"]'
listing_xpath = '//span[text()="Product Listings"]/parent::a'
export_xpath = '//button[@class="export-btn"]'

# Creating a new Chrome browser instance
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# Navigate to the website's login page
driver.get(website)

# Find the username field, enter the username and click login
email = driver.find_element(By.NAME, 'email').send_keys(username)
password = driver.find_element(By.NAME, 'password').send_keys(password.value)
login_button = driver.find_element(By.XPATH, login_xpath).click()

time.sleep(5)
wait = WebDriverWait(driver, 5)
close_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'modal-content__close')))
close_button.click()

# navigate to product listing
product_listings_button = wait.until(EC.element_to_be_clickable((By.XPATH, listing_xpath)))
product_listings_button.click()

time.sleep(10)

# List of ids of different checkbox options
checkbox_ids = ["export-All", "export-Active", "export-Inactive", "export-Sold Out", "export-Removed"]

# Iterating over the list and select each option
for id in checkbox_ids:
    button = wait.until(EC.element_to_be_clickable((By.XPATH, export_xpath))).click()
    checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[@for="{id}"]'))).click()

    export_button = driver.find_element(By.CLASS_NAME, "export-tooltip__btn").click()
    time.sleep(10)

driver.quit()
