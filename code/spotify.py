import os
import spotipy
from  spotipy import util as util
import json
import types


USER_NAME = '1182701610'
SCOPE = 'user-read-recently-played'
DATA_DIR = '../data'

def current_user_recently_played(self, limit=50):
    return self._get('me/player/recently-played', limit=limit)

token = util.prompt_for_user_token(
        USER_NAME,
        SCOPE,
        client_id='a0460ad67f0e41cd98bc7fde6bead6e9',
        client_secret='4aba3b0ea04d479eba656438b954c588',
        redirect_uri='http://localhost:9999/callback'
        )

spotify = spotipy.Spotify(auth=token)
spotify.current_user_recently_played = types.MethodType(current_user_recently_played, spotify)

recently_last_ver = 0
feats_last_ver = 0

for file in os.listdir(DATA_DIR):
    filename = os.fsdecode(file)
    if filename.endswith('.json'):
        if filename.startswith('recently'):
            recently_last_ver_next = int(filename.split('.')[0].split('_')[-1])
            if recently_last_ver_next > recently_last_ver:
                recently_last_ver = recently_last_ver_next
        if filename.startswith('audio'):
            feats_last_ver_next = int(filename.split('.')[0].split('_')[-1])
            if feats_last_ver_next > feats_last_ver:
                feats_last_ver = feats_last_ver_next

if recently_last_ver != feats_last_ver:
    print('Warning! not matching recent list with features')

recent_output = os.path.join(os.fsdecode(DATA_DIR), 'recently_played_'+str(recently_last_ver+1).zfill(3)+'.json')
print('saving file {}'.format(recent_output))
recently_played = spotify.current_user_recently_played(limit=50)
out_file = open(recent_output,"w")
out_file.write(json.dumps(recently_played, sort_keys=True, indent=2))
out_file.close()

for recent_song in recently_played['items']:
    print(recent_song['track']['artists'][0]['name'],
          recent_song['track']['name'],
          recent_song['played_at'],
          recent_song['track']['id'])

feats_output = os.path.join(os.fsdecode(DATA_DIR), 'audio_features_'+str(feats_last_ver+1).zfill(3)+'.json')
audio_features = {}
for recent_song in recently_played['items']:
    track_id = recent_song['track']['id']
    audio_features[track_id]=spotify.audio_features(track_id)

print('saving file {}'.format(feats_output))
out_file = open(feats_output,"w")
out_file.write(json.dumps(audio_features, sort_keys=True, indent=2))
out_file.close()
