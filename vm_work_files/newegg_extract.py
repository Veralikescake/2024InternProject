from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Connect VM with KV
keyVaultName = "vera-keys"
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)
password = client.get_secret("newegg-password")

website = "https://partner.newegg.com/euf/sellerportal/sign-in?returnUrl=https%3A%2F%2Fsellerportal.newegg.com%2Fv3"
username = "verahu@pconlineus.com"
username_id = "labeled-input-signEmail"
signin_button_id = 'signInSubmit'
password_id = 'labeled-input-password'
side_icon_xpath = '//euf-icons[@type="menu"]'
items_xpath = "//span[contains(text(), 'Items')]"
inventory_xpath = "//span[contains(text(), 'Pricing & Inventory')]"
export_xpath =  '//*[@id="mpsPageTopBar"]/div[2]/div/div/mps-list-header/div[1]/div/div[2]/div/div[6]/nz-form-item/nz-form-control/div/div/button'

# Creating a new Chrome browser instance
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# Navigate to the website's login page
driver.get(website)

# Find the username field, enter the username and click login
driver.switch_to.frame(0)
driver.find_element(By.ID, username_id).send_keys(username)
driver.find_element(By.ID, signin_button_id).click()

# switch back
driver.switch_to.default_content()

wait = WebDriverWait(driver, 5)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="content"]/iframe')))
# driver.switch_to.frame(0)
wait.until(EC.presence_of_element_located((By.ID, password_id))).send_keys(password.value)
wait.until(EC.element_to_be_clickable((By.ID, signin_button_id))).click()
# driver.find_element(By.ID, signin_button_id).click()

driver.switch_to.default_content()

# main page
wait = WebDriverWait(driver, 10)

wait.until(EC.element_to_be_clickable((By.XPATH, side_icon_xpath)))
driver.find_element(By.XPATH, side_icon_xpath).click()

wait.until(EC.element_to_be_clickable((By.XPATH, items_xpath)))
driver.find_element(By.XPATH, items_xpath).click()

wait.until(EC.element_to_be_clickable((By.XPATH, inventory_xpath)))
driver.find_element(By.XPATH, inventory_xpath).click()

# Path to the default 'Downloads' directory
download_dir = 'c:\\Users\\veraasadmin\\Downloads\\'
# Get the list of files before downloading
files_start = os.listdir(download_dir)

# Wait for the "Export" button to be clickable and click it
time.sleep(10)
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.XPATH, export_xpath)))
driver.find_element(By.XPATH, export_xpath).click()

# Wait for a new file to be downloaded
while True:
    time.sleep(1)  # Pause the execution for 1 second
    files_end = os.listdir(download_dir)
    if len(files_end) > len(files_start):
        break

# Get the name of the last downloaded file
downloaded_file = list(set(files_end) - set(files_start))[0]

# Full path to the downloaded file
downloaded_file_path = os.path.join(download_dir, downloaded_file) 

# Specify the new name for the file
new_file_name = 'inventory_newegg.xlsx'  # You can replace it by the name you want
new_file_path = os.path.join(download_dir, new_file_name)

# Rename the downloaded file
os.rename(downloaded_file_path, new_file_path)

driver.quit()
