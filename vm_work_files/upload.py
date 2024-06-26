import os
from azure.storage.blob import BlobServiceClient
import shutil
import  datetime
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Connect VM with KV
keyVaultName = "vera-keys"
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)
connect_str = client.get_secret("vera-connecting-string")

# Name of the Azure blob storage container
container_name = "daily-inventory"
# Local directory to upload 
download_dir = "c:\\Users\\veraasadmin\\Downloads"
archive_path = "C:\\Users\\veraasadmin\\Documents\\archive inventory"

try:
    blob_service_client = BlobServiceClient.from_connection_string(connect_str.value)

    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)
    
    # List all files in your local directory
    for file_name in os.listdir(download_dir):
        # Create a virtual directory with today's date
        today = datetime.date.today() 
        blob_name = today.strftime('%Y-%m-%d') +'/' + file_name
        blob_client = container_client.get_blob_client(blob_name)
        
        # Upload each file
        with open(os.path.join(download_dir, file_name),"rb") as data:
            blob_client.upload_blob(data)
    
    for file_name in os.listdir(download_dir):
        # Add a timestamp to the filename to make it unique before moving them to the archive folder
        base, extension = os.path.splitext(file_name)
        timestamp = datetime.datetime.now().strftime('%Y%m%d')
        new_file_name = f"{base}_{timestamp}{extension}"

        file_path = os.path.join(download_dir, file_name)
        destination_path = os.path.join(archive_path, new_file_name)
   
        # move the file
        shutil.move(file_path, destination_path)

except Exception as ex:
    print('Exception:')
    print(ex)
