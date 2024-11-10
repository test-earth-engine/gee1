import ee
import json
from google.oauth2 import service_account

service_account_key_file = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    service_account_key_file,
    scopes=['https://www.googleapis.com/auth/earthengine',
            'https://www.googleapis.com/auth/cloud-platform']
)

ee.Initialize(credentials)
print("[earth_tools]", ee.String('Hello from the Earth Engine servers!').getInfo())
