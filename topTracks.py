import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Setup your own app on the Spotify Development site
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="227729d94cc840b98e795a4d29885e5a",
                                               client_secret="4ba1f9d35d4c43029d8cc041705528e8",
                                               redirect_uri="https://example.com/callback/",
                                               scope="user-library-read playlist-modify-private \
                                                        playlist-modify \
                                                        playlist-modify-public \
                                                        playlist-read-collaborative \
                                                        user-top-read")) # Permissions needed to modify
                                                                         # your playlists
# These can be obtained by right clicking on a playlist
# in Spotify (on a desktop) and hitting the "Share -> copy URI".
DestPlaylistURI = 'spotify:playlist:5rLUtwECq9xqptuFQR8P1b'
DestPlaylistID = '5rLUtwECq9xqptuFQR8P1b'
user = 'diversecity2014'



def getPopPlaylistSongs():
    i = 0 # for debugging and printing
    i2 = 0 # for debbuging and printing
    results = sp.featured_playlists(locale='en_US', country='US', limit=50, offset=0)
    # Loops through the featured-plalists on spotify
    for item in results['playlists']['items']:
        playlist = sp.playlist(item['id'])['tracks']
        tracks = playlist['items']
        while playlist['next']:
            playlist = sp.next(playlist)
            tracks.extend(playlist['items'])
        #print(playlist)
        # Loops through each track in the playlist
        for trackI in tracks:
            idx = 0
            track = trackI['track']
            if track is None:
                continue
            artist = sp.artist(track['artists'][0]['id'])
            genres = artist['genres']
            # If track has a 73% popularity or better, add song to new playlist called 
            # I also added a filter for country music, you can remove this by taking away the and statemtn and the code after
            if track['popularity'] > 73 and 'contemporary country' not in genres:
                sp.playlist_add_items(playlist_id=DestPlaylistURI, items=[track['uri']], position=None)
                print(i, "Added: ->", idx+i2, track['artists'][0]['name'], "–", track['name'], "–",track['popularity'])
                idx+=1
            i+=1
        i2 +=100

#deletes from playlist to restart adding process
index = 0
results = sp.playlist(DestPlaylistID)['tracks']
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])
for item in tracks:
        sp.user_playlist_remove_all_occurrences_of_tracks(user=user, playlist_id=DestPlaylistID, tracks=[item['track']['uri']])
        print("Song Deleted", index)
        index += 1

#adds new songs
getPopPlaylistSongs()
