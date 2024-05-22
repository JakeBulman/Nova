import requests
import msal

def request_access_token():
    app_id = '43f6b8dc-2c27-4968-aa46-091e78ce7224'
    tenant_id = '75d6cc78-71b9-42e6-aa2a-b9889a0f080f'

    

    authority_url = 'https://login.microsoftonline.com/' + tenant_id
    scopes = ['https://analysis.windows.net/powerbi/api/.default']

    # Step 1. Generate Power BI Access Token
    client = msal.PublicClientApplication(app_id, authority=authority_url)
    token_response = client.acquire_token_by_username_password(username=username, password=password, scopes=scopes)
    if not 'access_token' in token_response:
        raise Exception(token_response['error_description'])

    access_id = token_response.get('access_token')
    return access_id

access_id = request_access_token()

dataset_id = 'b3d4aae5-b55f-4568-84ee-099c873be795'
endpoint = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes'
headers = {
    'Authorization': f'Bearer ' + access_id
}

response = requests.post(endpoint, headers=headers)
if response.status_code == 202:
    print('Dataset refreshed')
else:
    print(response.reason)
    print(response.json())
