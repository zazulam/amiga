import boto3 
import os
import spotipy
import spotipy.util as util
from table_validator import *


ssm = boto3.client('ssm')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    if validate_table():
        id = ssm.get_parameter(Name='spotify-mesh-clientId',WithDecryption=True)['Parameter']['Value']
        secret = ssm.get_parameter(Name='spotify-mesh-secret',WithDecryption=True)['Parameter']['Value']
        callback = ssm.get_parameter(Name='spotify-mesh-callback',WithDecryption=True)['Parameter']['Value']
        scope = ssm.get_parameter(Name='spotify-mesh-scope',WithDecryption=True)['Parameter']['Value']

        token = util.prompt_for_user_token(username=os.environ['USERNAME'],scope=scope,client_id=id,client_secret=secret,redirect_uri=callback)
        sp_user = spotipy.Spotify(auth=token)
        
        playlists = sp_user.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == os.environ['PLAYLIST_NAME']:
                track_uris = []
                tracks = sp_user.playlist_tracks(playlist['id'])
                for track in tracks['items']:
                    print(track['track']['id'] +': '+ track['track']['artists'][0]['name']+': '+track['track']['name'])
                    song_item = {
                        'Track_Id':{'S':track['track']['id']},
                        'Artist':{'S':track['track']['artists'][0]['name']},
                        'Title':{'S':track['track']['name']},
                        'URI':{'S':track['track']['uri']}
                    }
                    dynamodb.put_item(TableName=os.environ["SPOTIFY_TABLE_NAME"],Item=song_item)
                    track_uris.append(track['track']['uri'])
                sp_user.user_playlist_remove_all_occurrences_of_tracks(os.environ['USERNAME'],playlist['id'],track_uris)
        return 200
    else:
        return 503