import json
import os

def jdefault(o):
    return o.__dict__

def credentials():
    data = json.loads(os.environ['CREDENTIALS_FILE'])
    with open('credentials.json', 'w') as file:
        file.write(json.dumps(data, default=jdefault))

def secrets():
    data = json.loads(os.environ['CLIENT_SECRET_FILE'])
    with open('client_secrets.json', 'w') as file:
        file.write(json.dumps(data, default=jdefault))
    credentials()

def settings():
    with open('settings.yaml', 'w') as file:
        file.write('client_config_backend: settings\n\
client_config:\n\
  client_id: {}\n\
  client_secret: {}\n\
\n\
save_credentials: True\n\
save_credentials_backend: file\n\
save_credentials_file: credentials.json\n\
\n\
get_refresh_token: True\n\
\n\
oauth_scope:\n\
  - https://www.googleapis.com/auth/drive.file\n\
  - https://www.googleapis.com/auth/drive.install'.format(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET']))
    secrets()
        
settings()


