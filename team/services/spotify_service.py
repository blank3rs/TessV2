import os
import time
import spotipy
import pyautogui
from spotipy.oauth2 import SpotifyOAuth
from team.utils.app_manager import open_local_app
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

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
        results = spotify.search(q=query, type='track', limit=10)
        if results['tracks']['items']:
            sorted_tracks = sorted(results['tracks']['items'], key=lambda x: x['popularity'], reverse=True)
            track = sorted_tracks[0]
            try:
                spotify.start_playback(uris=[track['uri']])
                return f"Playing {track['name']} by {track['artists'][0]['name']}"
            except Exception as e:
                if "No active device found" in str(e):
                    open_local_app("spotify")
                    time.sleep(2)
                    pyautogui.press('space')
                    time.sleep(2)
                    
                    max_retries = 3
                    for _ in range(max_retries):
                        try:
                            spotify.start_playback(uris=[track['uri']])
                            return f"Playing {track['name']} by {track['artists'][0]['name']}"
                        except Exception:
                            time.sleep(1)
                            continue
                    
                    return f"Failed to play {track['name']} after multiple attempts. Please check if Spotify is running properly."
                else:
                    raise e
        return "Song not found. Please try a different query."
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

def spotify_pause_song() -> str:
    """Pause the currently playing song"""
    try:
        spotify.pause_playback()
        return "Paused the current song."
    except Exception as e:
        return f"Error pausing song: {str(e)}"

def spotify_add_to_liked(track_uri: str) -> str:
    """Add a song to the user's liked songs"""
    if not track_uri:
        return "Invalid track URI provided."
    try:
        spotify.current_user_saved_tracks_add(tracks=[track_uri])
        logging.info(f"Added track {track_uri} to liked songs.")
        return "Song added to liked songs."
    except Exception as e:
        logging.error(f"Error adding song to liked: {str(e)}")
        return f"Error adding song to liked: {str(e)}"

def is_song_playing() -> bool:
    """Check if a song is currently playing"""
    try:
        current = spotify.current_user_playing_track()
        return current is not None and current['is_playing']
    except Exception as e:
        logging.error(f"Error checking playback state: {str(e)}")
        return False

def spotify_suggest_and_play_song(query: str) -> str:
    """Suggest and play a song based on the user's query."""
    try:
        results = spotify.search(q=query, type='track', limit=5)  # Get multiple suggestions
        if results['tracks']['items']:
            # Sort results by popularity
            sorted_tracks = sorted(results['tracks']['items'], key=lambda x: x['popularity'], reverse=True)
            track = sorted_tracks[0]  # Select the most popular track
            spotify.start_playback(uris=[track['uri']])
            return f"Playing suggested song: {track['name']} by {track['artists'][0]['name']}"
        return "No songs found for your query. Please try a different one."
    except Exception as e:
        return f"Error suggesting and playing song: {str(e)}" 