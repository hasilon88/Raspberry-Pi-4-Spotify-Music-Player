import base64
import requests
import json

# --- Retrieving API Keys ---

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def get_string_values_from_json(json_data):
    string_values = {}
    for key, value in json_data.items():
        string_values[key] = str(value)
    return string_values

# Read API keys from json file
json_file_path = 'api-secret.json'
api_keys = read_json_file(json_file_path)

CLIENT_ID = api_keys.get('CLIENT_ID')
CLIENT_SECRET = api_keys.get('CLIENT_SECRET')
REDIRECT_URI = api_keys.get('REDIRECT_URI')

# --- Setup ---

def getUserCode():
    SCOPE = 'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-read user-library-modify user-top-read user-read-recently-played user-follow-read user-follow-modify user-read-private user-read-email user-library-read user-library-modify'
    SCOPE = SCOPE.replace(" ", "+")

    authorize_url = 'https://accounts.spotify.com/authorize'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }

    authorization_url = f"{authorize_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

    print(f"Please visit the following URL to authorize your application:\n{authorization_url}")

def convertCodeToToken(AUTHORIZATION_CODE):
    authorization_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': AUTHORIZATION_CODE,
        'redirect_uri': REDIRECT_URI,
    }

    headers = {
        'Authorization': f'Basic {authorization_header}',
    }

    response = requests.post(token_url, data=token_data, headers=headers)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get('access_token')
        refresh_token = token_info.get('refresh_token')
        token_type = token_info.get('token_type')
        expires_in = token_info.get('expires_in')
        
        print(f"Access Token: {access_token}")
        print(f"Refresh Token: {refresh_token}")
        print(f"Token Type: {token_type}")
        print(f"Expires In: {expires_in} seconds")
    else:
        print("Failed to obtain access token.")
    
    return access_token

# --------------

def getCurrentPlayingSong():
    current_track_url = 'https://api.spotify.com/v1/me/player/currently-playing'

    headers = {
        'Authorization': f'Bearer {USER_TOKEN}',
    }

    response = requests.get(current_track_url, headers=headers)

    if response.status_code == 200:
        current_track_data = response.json()

        return {
            'track_name': current_track_data.get('item', {}).get('name'),
            'artist_names': [artist['name'] for artist in current_track_data.get('item', {}).get('artists', [])],
            'album_name': current_track_data.get('item', {}).get('album', {}).get('name')
        }
    
    else:
        print("Failed to fetch currently playing track data.\nError code: ", response.status_code)

def togglePlay():
    current_playback_url = 'https://api.spotify.com/v1/me/player'
    
    headers = {
        'Authorization': f'Bearer {USER_TOKEN}',
    }
    
    response = requests.get(current_playback_url, headers=headers)

    if response.status_code == 200:
        playback_data = response.json()

        is_playing = playback_data.get('is_playing')

        if is_playing:
            action_url = 'https://api.spotify.com/v1/me/player/pause'
        else:
            action_url = 'https://api.spotify.com/v1/me/player/play'
        
        action_response = requests.put(action_url, headers=headers)
        
        if action_response.status_code != 204:
            print("Failed to toggle pause/play.")    

    else:
        print("Failed to fetch current playback data.")

def nextSong():
    next_track_url = 'https://api.spotify.com/v1/me/player/next'

    headers = {
        'Authorization': f'Bearer {USER_TOKEN}',
    }

    response = requests.post(next_track_url, headers=headers)

    if response.status_code != 204:
        print("Failed to skip to the next track.")

def previousSong():
    next_track_url = 'https://api.spotify.com/v1/me/player/previous'

    headers = {
        'Authorization': f'Bearer {USER_TOKEN}',
    }

    response = requests.post(next_track_url, headers=headers)

    if response.status_code != 204:
        print("Failed to skip to the next track.")
