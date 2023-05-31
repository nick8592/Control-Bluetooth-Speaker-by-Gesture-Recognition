from googleapiclient.http import MediaFileUpload
from Google import create_service

CLIENT_SECRET_FILE = 'client_secret_280883005885-hl8ho63vaaeb4ph2tso85rj6t7qkprog.apps.googleusercontent.com.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

folder_id = '1MLyLxexMCusU4l4bAw9OfIGCIhqGE5uC'
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
file_id = '1XMlrvZwkiSxLnwqaP36r7KKxerR7EA4z'

media_content = MediaFileUpload('music_log.txt', mimetype='text/plain')

def api_upload():
    service.files().update(
        fileId=file_id,
        media_body=media_content
    ).execute()
    
api_upload()
