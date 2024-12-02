import os
import time
import spotipy
import pyautogui
from spotipy.oauth2 import SpotifyOAuth
from ..utils.app_manager import open_local_app

# Initialize Spotify client
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-library-read user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private user-read-currently-playing"
))

def spotify_play_song(query: str) -> str:
    """Play a song on Spotify"""
    try:
        results = spotify.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            try:
                spotify.start_playback(uris=[track['uri']])
                return f"Playing {track['name']} by {track['artists'][0]['name']}"
            except Exception as e:
                if "No active device found" in str(e):
                    # Open Spotify and press space to activate
                    open_local_app("spotify")
                    time.sleep(2)  # Wait for Spotify to open
                    pyautogui.press('space')  # Press space to play/pause
                    time.sleep(1)  # Wait a moment
                    # Try playing again
                    spotify.start_playback(uris=[track['uri']])
                    return f"Playing {track['name']} by {track['artists'][0]['name']}"
                else:
                    raise e
        return "Song not found"
    except Exception as e:
        return f"Error playing song: {str(e)}"

def spotify_current_track() -> str:
    """Get currently playing track"""
    try:
        current = spotify.current_user_playing_track()
        if current and current['item']:
            track = current['item']
            return f"Currently playing: {track['name']} by {track['artists'][0]['name']}"
        return "Nothing is currently playing"
    except Exception as e:
        return f"Error getting current track: {str(e)}"

def spotify_create_playlist(name: str, description: str = "") -> str:
    """Create a new Spotify playlist"""
    try:
        user_id = spotify.current_user()['id']
        playlist = spotify.user_playlist_create(user_id, name, public=True, description=description)
        return f"Created playlist: {playlist['name']}"
    except Exception as e:
        return f"Error creating playlist: {str(e)}" 