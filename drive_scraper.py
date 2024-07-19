import psycopg2
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()

# Service account credentials
credentials = service_account.Credentials.from_service_account_file('service_account_key.json')

# Create a service object
service = build('drive', 'v3', credentials=credentials)

# Function to connect to PostgreSQL database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("POSTGRESQL_DATABASE"),
            user=os.environ.get("POSTGRESQL_USERNAME"),
            password=os.environ.get("POSTGRESQL_PASSWORD"),
            host=os.environ.get("POSTGRESQL_HOST"),
            port=os.environ.get("POSTGRESQL_PORT")
        )
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database.")
        print(e)
        return None

# Function to list all files and folders recursively within a specific folder
def list_files_and_folders(folder_id, conn, cursor):
    results = service.files().list(q=f"'{folder_id}' in parents", fields="files(name, mimeType, id)").execute()
    files = results.get('files', [])
    
    if files:
        for file in files:
            if 'id' in file:
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    print("Current Folder:", file['name'])
                    list_files_and_folders(file['id'], conn, cursor)
                else:
                    file_name = file['name']
                    print("\t\t\tFile processed:",file_name)
                    download_link = f"https://drive.google.com/uc?id={file['id']}"
                    insert_query = "INSERT INTO files (file_name, download_link) VALUES (%s, %s)"
                    cursor.execute(insert_query, (file_name, download_link))
                    conn.commit()

# Example usage
folder_id = '11ywkOKyeixCPihsCzqZDyzy2msLXxx6w'  # Replace with the folder ID
print("Listing all folders and files within the specified folder:")

conn = connect_to_database()
if conn:
    cursor = conn.cursor()
    list_files_and_folders(folder_id, conn, cursor)
    cursor.close()
    conn.close()
    print("Files and URLs stored in the database.")
else:
    print("Unable to connect to the database.")
