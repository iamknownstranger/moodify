# export SPOTIPY_CLIENT_ID='650afbef135d47259ff2c8dfbdb7affa'
# export SPOTIPY_CLIENT_SECRET='7b2ad9455feb43b29355e442a9035767'
# export SPOTIPY_REDIRECT_URI='https://open.spotify.com/'

from sklearn.preprocessing import MinMaxScaler
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt
# plt.style.use('dark_background')

from math import pi


SPOTIPY_CLIENT_ID = '650afbef135d47259ff2c8dfbdb7affa'
SPOTIPY_CLIENT_SECRET = '7b2ad9455feb43b29355e442a9035767'
SPOTIPY_REDIRECT_URI = 'https://share.streamlit.io/iamknownstranger/moodify/main/moodify.py'


scope = "user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                     client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))


playlist = sp.current_user_recently_played()

# create a list of song ids
track_ids = []

for item in playlist['items']:
    track_id = item['track']['id']
    if track_id not in track_ids:
        track_ids.append(track_id)

track_meta_data = {'id': [], 'album': [], 'name': [],
                   'artist': [], 'explicit': [], 'popularity': []}

streamlit_data = {'track_id':[], 'track_name': [], 'images': [], 'album_name': [
], 'artist': [], 'album_uri':[], 'external_urls': [], 'href': [], 'uri': []}


for track_id in track_ids:
    # get song's meta data
    meta = sp.track(track_id)

    streamlit_data['track_name'].append(meta['name'])
    streamlit_data['track_id'].append(track_id)
    streamlit_data['images'].append(meta['album']['images'][0]['url'])

    streamlit_data['album_name'].append(meta['album']['name'])
    streamlit_data['artist'].append(meta['album']['artists'])
    streamlit_data['external_urls'].append(meta['external_urls'])
    streamlit_data['href'].append(meta['album']['href'])
    streamlit_data['uri'].append(meta['uri'])
    streamlit_data['album_uri'].append(meta['album']['id'])

    # song id
    track_meta_data['id'].append(track_id)

    # album name
    album = meta['album']['name']
    track_meta_data['album'] += [album]

    # song name
    song = meta['name']
    track_meta_data['name'] += [song]

    # artists name
    s = ', '
    artist = s.join([singer_name['name'] for singer_name in meta['artists']])
    track_meta_data['artist'] += [artist]

    # explicit: lyrics could be considered offensive or unsuitable for children
    explicit = meta['explicit']
    track_meta_data['explicit'].append(explicit)

    # song popularity
    popularity = meta['popularity']
    track_meta_data['popularity'].append(popularity)

data = pd.DataFrame.from_dict(streamlit_data)

track_meta_data_df = pd.DataFrame.from_dict(track_meta_data)

# check the song feature
features = sp.audio_features(track_meta_data['id'])
# change dictionary to dataframe
features_df = pd.DataFrame.from_dict(features)

# convert milliseconds to mins
# duration_ms: The duration of the track in milliseconds.
# 1 minute = 60 seconds = 60 × 1000 milliseconds = 60,000 ms
features_df['duration_ms'] = features_df['duration_ms']/60000

# combine two dataframe
final_df = track_meta_data_df.merge(features_df)

music_feature = features_df[['danceability', 'energy', 'loudness', 'speechiness',
                             'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                             'duration_ms']].copy()
min_max_scaler = MinMaxScaler()
music_feature.loc[:] = min_max_scaler.fit_transform(music_feature.loc[:])




# convert column names into a list
categories = list(music_feature.columns)
# number of categories
N = len(categories)

# create a list with the average of all features
value = list(music_feature.mean())

# repeat first value to close the circle
# the plot is a circle, so we need to "complete the loop"
# and append the start value to the end.
value += value[:1]
# calculate angle for each category
angles = [n/float(N)*2*pi for n in range(N)]
angles += angles[:1]


# plot
chart = plt.figure()
chart.set_facecolor('#0E1117')
ax = chart.add_subplot(projection='polar')
ax.set_facecolor('#0E1117')
ax.scatter(angles, value)
plt.fill(angles, value)

plt.xticks(angles[:-1], categories, size=15, color='white')
plt.yticks(color='white', size=15)

plt.savefig('output.png')
