from googleapiclient.http import MediaFileUpload
from Google import create_service

CLIENT_SECRET_FILE = 'client_secret_366059386253-48toeau80e9r2e2chma3r55ogdv13pg5.apps.googleusercontent.com.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

folder_id = '177Eq_W1B8ZlARaqaCHQVMkjdelhEZ9Lm'
file_name = 'music_log.txt'
mime_type = 'text/plain'

# # Upload a file
# file_metadata = {
#     'name': file_name,
#     'parents': [folder_id]
# }
# 
# media_content = MediaFileUpload(file_name, mimetype=mime_type)
# 
# service.files().create(
#     body=file_metadata,
#     media_body=media_content
# ).execute()

# Replace Existing File on Google Drive
file_id = '12w1n8HVAR5KE3YWp7jUF4FL2KvZsIxg8'

media_content = MediaFileUpload('music_log.txt', mimetype='text/plain')

def api_upload():
    service.files().update(
        fileId=file_id,
        media_body=media_content
    ).execute()
    
api_upload()
