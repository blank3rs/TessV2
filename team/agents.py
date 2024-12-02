from swarm import Swarm, Agent
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from googlesearch import search
import webbrowser
import requests
from bs4 import BeautifulSoup
import re
import subprocess
import platform
from typing import Optional
import pyautogui
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

# First create the Azure OpenAI client
azure_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Initialize Swarm with the Azure OpenAI client
client = Swarm(
    client=azure_client
)

# Declare global variable
current_agent = None

class AgentWithMemory:
    def __init__(self, agent, max_memory=10):
        self.agent = agent
        self.memory = []
        self.max_memory = max_memory
        self.last_search_results = []
        self.last_content_results = []
    
    def add_to_memory(self, message):
        self.memory.append(message)
        # Keep only the last max_memory messages
        if len(self.memory) > self.max_memory:
            self.memory = self.memory[-self.max_memory:]
    
    def get_memory(self):
        return self.memory

# Add transfer function for Search Agent
def transfer_to_SearchAgent():
    global current_agent
    print("Transferred to Search Agent")
    current_agent = agents["Search Agent"]
    return current_agent.agent

# Update the transfer functions to include Search Agent as an option
def transfer_to_GeneralTess():
    global current_agent
    print("Transferred to General Tess")
    current_agent = agents["General Tess"]
    return current_agent.agent

def transfer_to_TeacherTess():
    global current_agent
    print("Transferred to Teacher Tess")
    current_agent = agents["Teacher Tess"]
    return current_agent.agent

# Add these function definitions after the transfer_to_TeacherTess function and before the agent definitions

def transfer_to_AppManager():
    global current_agent
    print("Transferred to App Manager")
    current_agent = agents["App Manager"]
    return current_agent.agent

def transfer_to_EmailAgent():
    global current_agent
    print("Transferred to Email Agent")
    current_agent = agents["Email Agent"]
    return current_agent.agent

def open_local_app(app_name: str) -> str:
    """
    Opens a local application using Windows search or OS-specific commands
    """
    system = platform.system().lower()
    
    try:
        if system == "windows":
            # Press Windows key
            pyautogui.press('win')
            time.sleep(0.5)  # Wait for search to open
            
            # Type the app name
            pyautogui.write(app_name)
            time.sleep(0.5)  # Wait for search results
            
            # Press enter to launch the first result
            pyautogui.press('enter')
            
            # Since pyautogui commands completed successfully, we can assume the app launched
            return f"Successfully launched {app_name}"
            
        elif system == "darwin":  # macOS
            subprocess.Popen(["open", "-a", app_name])
            return f"Successfully launched {app_name} on macOS"
            
        elif system == "linux":
            subprocess.Popen([app_name.lower()])
            return f"Successfully launched {app_name} on Linux"
    
    except Exception as e:
        return f"Error launching {app_name}: {str(e)}"

def find_and_open_web_app(app_name: str) -> str:
    """
    Searches for and opens a web application using Google search
    """
    try:
        # Extensive dictionary of common web apps and their direct URLs
        direct_urls = {
            # Google Services
            'gmail': 'https://mail.google.com',
            'google mail': 'https://mail.google.com',
            'google drive': 'https://drive.google.com',
            'google docs': 'https://docs.google.com',
            'google sheets': 'https://sheets.google.com',
            'google slides': 'https://slides.google.com',
            'google calendar': 'https://calendar.google.com',
            'google photos': 'https://photos.google.com',
            'google maps': 'https://maps.google.com',
            'google meet': 'https://meet.google.com',
            
            # Microsoft Services
            'outlook': 'https://outlook.live.com',
            'hotmail': 'https://outlook.live.com',
            'onedrive': 'https://onedrive.live.com',
            'office': 'https://www.office.com',
            'office 365': 'https://www.office.com',
            'teams': 'https://teams.microsoft.com',
            
            # Social Media
            'facebook': 'https://www.facebook.com',
            'instagram': 'https://www.instagram.com',
            'twitter': 'https://twitter.com',
            'x': 'https://twitter.com',
            'linkedin': 'https://www.linkedin.com',
            'pinterest': 'https://www.pinterest.com',
            'reddit': 'https://www.reddit.com',
            'tiktok': 'https://www.tiktok.com',
            
            # Video/Streaming
            'youtube': 'https://www.youtube.com',
            'netflix': 'https://www.netflix.com',
            'prime video': 'https://www.amazon.com/prime-video',
            'disney plus': 'https://www.disneyplus.com',
            'disney+': 'https://www.disneyplus.com',
            'hulu': 'https://www.hulu.com',
            'twitch': 'https://www.twitch.tv',
            
            # Shopping
            'amazon': 'https://www.amazon.com',
            'ebay': 'https://www.ebay.com',
            'walmart': 'https://www.walmart.com',
            'target': 'https://www.target.com',
            'etsy': 'https://www.etsy.com',
            
            # Productivity/Work
            'slack': 'https://slack.com',
            'trello': 'https://trello.com',
            'notion': 'https://www.notion.so',
            'asana': 'https://app.asana.com',
            'jira': 'https://www.atlassian.com/software/jira',
            'zoom': 'https://zoom.us',
            
            # Cloud Storage
            'dropbox': 'https://www.dropbox.com',
            'box': 'https://www.box.com',
            
            # Education
            'kahoot': 'https://kahoot.com',
            'coursera': 'https://www.coursera.org',
            'udemy': 'https://www.udemy.com',
            'duolingo': 'https://www.duolingo.com',
            
            # Finance
            'paypal': 'https://www.paypal.com',
            'venmo': 'https://venmo.com',
            'mint': 'https://mint.intuit.com',
            
        }
        
        # Clean and check input
        app_name_lower = app_name.lower().strip()
        
        # Check if it's in our direct URLs
        if app_name_lower in direct_urls:
            webbrowser.open_new_tab(direct_urls[app_name_lower])
            return f"Opened {app_name} at {direct_urls[app_name_lower]}"
        
        # Try to construct a URL for common patterns
        if not app_name_lower.startswith(('http://', 'https://')):
            # Remove spaces and special characters
            clean_name = ''.join(c for c in app_name_lower if c.isalnum())
            
            # Try common URL patterns
            potential_urls = [
                f"https://www.{clean_name}.com",
                f"https://{clean_name}.com",
                f"https://app.{clean_name}.com",
                f"https://{clean_name}.io",
                f"https://www.{clean_name}.io"
            ]
            
            # Try each potential URL
            for url in potential_urls:
                try:
                    response = requests.head(url, timeout=2)
                    if response.status_code == 200:
                        webbrowser.open_new_tab(url)
                        return f"Opened {app_name} at {url}"
                except:
                    continue
        
        # If direct URLs and constructed URLs fail, fall back to search
        search_query = f"{app_name} login official site"
        results = search(search_query, num_results=1)
        
        for url in results:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open_new_tab(url)
            return f"Opened {app_name} at {url}"
            
        return f"Could not find official website for {app_name}"
    except Exception as e:
        return f"Error opening web app: {str(e)}"

# Create the base agents
GeneralTess = Agent(
    name="General Tess",
    instructions="""You are a general assistant who can answer basic questions. Transfer to:
    - TeacherTess for educational topics
    - SearchAgent when users need current information
    - AppManager when users want to open applications, web services, or handle email operations
    Do not transfer for casual mentions. Call the appropriate transfer function when needed.
    ALWAYS transfer to AppManager for ANY email-related requests.""",
    model="gpt-4o-mini",
    functions=[transfer_to_TeacherTess, transfer_to_SearchAgent, transfer_to_AppManager],
)

TeacherTess = Agent(
    name="Teacher Tess",
    instructions="""You are a teacher who can answer questions about education. Transfer to:
    - GeneralTess for non-educational topics
    - SearchAgent for specific course information
    - AppManager when users want to open educational applications or services
    Call the appropriate transfer function when needed.""",
    model="gpt-4o-mini",
    functions=[transfer_to_GeneralTess, transfer_to_SearchAgent, transfer_to_AppManager],
)

def scrape_url(url):
    """
    Scrape content from a URL and return cleaned text
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit text length to avoid token limits
        return text[:2000]  # Adjust length as needed
    except Exception as e:
        return f"Error scraping URL: {str(e)}"

def search_web(query):
    """
    Search the web using Google Search and scrape content
    """
    print("Searching and reading content...")
    try:
        search_results = []
        content_results = []
        
        for result in search(query, num_results=3):
            search_results.append(result)
            content = scrape_url(result)
            content_results.append({
                'url': result,
                'content': content
            })
            
        # Store both URLs and content in the current agent's memory
        current_agent.last_search_results = search_results
        current_agent.last_content_results = content_results
        
        return content_results
    except Exception as e:
        return f"Error performing search: {str(e)}"

def open_urls(urls=None):
    print("*************")
    print(f"\n\n{urls}\n\n")
    print("*************")

    """
    Open a list of URLs in the default web browser
    Parameters:
        urls: Can be either a list of URLs, a single URL string, or a number (1-3) 
             referring to the last search results
    """
    print("Opening...")
    
    try:
        # Handle case where a specific result number is requested
        if isinstance(urls, (int, str)) and str(urls).isdigit():
            index = int(urls) - 1  # Convert to 0-based index
            if 0 <= index < len(current_agent.last_search_results):
                url = current_agent.last_search_results[index]
                # Ensure URL starts with http:// or https://
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                webbrowser.get('chrome').open_new_tab(url)
                return f"Opened URL: {url}"
            return "Invalid result number"
        
        # Handle case where specific URLs are provided
        if urls:
            if isinstance(urls, str):
                urls = [urls]  # Convert single URL to list
            
            opened_count = 0
            for url in urls:
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                try:
                    webbrowser.get('chrome').open_new_tab(url)
                    opened_count += 1
                except webbrowser.Error:
                    # Fallback to default browser if Chrome is not available
                    webbrowser.open_new_tab(url)
                    opened_count += 1
            
            return f"Successfully opened {opened_count} URLs in your browser"
        
        return "No URLs provided to open"
        
    except Exception as e:
        return f"Error opening URLs: {str(e)}"
    
    # Add these transfer functions with the other transfer functions
def transfer_to_SpotifyAgent():
    global current_agent
    print("Transferred to Spotify Agent")
    current_agent = agents["Spotify Agent"]
    return current_agent.agent

# Update the search agent with improved instructions
search_agent = Agent(
    name="Search Agent",
    instructions="""You are a search agent that can search the internet and read webpage content. Transfer to:
    - GeneralTess for general queries
    - TeacherTess for educational discussions
    - AppManager when users want to open applications or web services
    Base answers only on actual content returned from websites.""",
    model="gpt-4o-mini",
    functions=[search_web, open_urls, transfer_to_GeneralTess, 
               transfer_to_TeacherTess, transfer_to_AppManager],
)

# Add this after the existing agent definitions

AppManager = Agent(
    name="App Manager",
    instructions="""You are an App Manager that can open both local and web applications. When handling requests:

    1. For desktop applications that are typically installed locally, use open_local_app():
       Examples: Spotify, Discord, Chrome, Word, Excel, Calculator, Notepad
       
    2. For web-based services, use find_and_open_web_app():
       Examples: Gmail, YouTube, Google Drive, Outlook, Google Docs, LinkedIn, Twitter
       
    3. For ambiguous cases, prefer web version first, then fall back to local:
       - If a service is primarily web-based (like Gmail), use find_and_open_web_app()
       - If the web version fails or it's clearly a desktop app, use open_local_app()
    
    4. For specific service requests:
       - Transfer to SpotifyAgent for music control
       - Gmail is for personal email
       - Outlook is for school email
    
    Transfer to:
    - GeneralTess for general queries
    - TeacherTess for educational topics
    - SearchAgent for information gathering
    - SpotifyAgent for music control
    
    When an app is launched successfully, provide positive confirmation.""",
    model="gpt-4o-mini",
    functions=[
        open_local_app,
        find_and_open_web_app,
        transfer_to_GeneralTess,
        transfer_to_TeacherTess,
        transfer_to_SearchAgent,
        transfer_to_SpotifyAgent
    ],
)

# Initialize Spotify client
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-library-read user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private user-read-currently-playing"
))



# Add these Spotify control functions
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

# Add this new agent definition before the agents dictionary
SpotifyAgent = Agent(
    name="Spotify Agent",
    instructions="""You are a Spotify assistant that can control music playback and manage playlists. You can:
    1. Play specific songs using spotify_play_song()
    2. Check currently playing track using spotify_current_track()
    3. Create playlists using spotify_create_playlist()
    
    Transfer to:
    - GeneralTess for non-music queries
    - SearchAgent for web searches about music
    - AppManager for opening other applications
    
    Always confirm actions with users and provide feedback about what's playing or what was created.""",
    model="gpt-4o-mini",
    functions=[
        spotify_play_song,
        spotify_current_track,
        spotify_create_playlist,
        transfer_to_GeneralTess,
        transfer_to_SearchAgent,
        transfer_to_AppManager
    ],
)

# Add these email functions before the agent definitions
def read_emails(email_provider="gmail", folder="inbox", limit=5) -> str:
    """Read recent emails from the specified folder"""
    try:
        # Get email credentials based on provider
        if email_provider.lower() == "gmail":
            email_address = os.getenv("GMAIL_ADDRESS")
            email_password = os.getenv("GMAIL_PASSWORD")
            imap_server = "imap.gmail.com"
        elif email_provider.lower() == "outlook":
            email_address = os.getenv("OUTLOOK_ADDRESS")
            email_password = os.getenv("OUTLOOK_PASSWORD")
            imap_server = "outlook.office365.com"
        else:
            return f"Unsupported email provider: {email_provider}"
        
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, email_password)
        
        # Select the folder (mailbox)
        mail.select(folder)
        
        # Search for all emails and get the latest ones
        _, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        latest_emails = email_ids[-limit:] if len(email_ids) > limit else email_ids
        
        email_list = []
        for email_id in reversed(latest_emails):
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            email_body = msg_data[0][1]
            message = email.message_from_bytes(email_body)
            
            subject = message["subject"]
            sender = message["from"]
            date = message["date"]
            
            email_list.append(f"From: {sender}\nSubject: {subject}\nDate: {date}\n")
        
        mail.close()
        mail.logout()
        
        return "\n".join(email_list) if email_list else "No emails found"
    except Exception as e:
        return f"Error reading emails: {str(e)}"

def send_email(to: str, subject: str, body: str, email_provider="gmail") -> str:
    """Send an email"""
    try:
        # Get email credentials based on provider
        if email_provider.lower() == "gmail":
            email_address = os.getenv("GMAIL_ADDRESS")
            email_password = os.getenv("GMAIL_PASSWORD")
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
        elif email_provider.lower() == "outlook":
            email_address = os.getenv("OUTLOOK_ADDRESS")
            email_password = os.getenv("OUTLOOK_PASSWORD")
            smtp_server = "smtp.office365.com"
            smtp_port = 587
        else:
            return f"Unsupported email provider: {email_provider}"
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = to
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return f"Email sent successfully to {to} using {email_provider}"
    except Exception as e:
        return f"Error sending email: {str(e)}"

# Update the EmailAgent instructions to include provider information
EmailAgent = Agent(
    name="Email Agent",
    instructions="""You are an email assistant that can read and send emails from both Gmail (personal) and Outlook (school) accounts. You can:
    1. Read recent emails using read_emails(email_provider="gmail"|"outlook")
    2. Send emails using send_email(to, subject, body, email_provider="gmail"|"outlook")
    
    Remember:
    - Gmail is for personal email
    - Outlook is for school email
    
    Always ask or confirm which email provider the user wants to use if not specified.
    If the context involves school-related matters, suggest using Outlook.
    If the context is personal, suggest using Gmail.
    
    Transfer to:
    - GeneralTess for non-email queries
    - SearchAgent for web searches
    - AppManager for opening other applications
    
    Always confirm actions with users and provide feedback about email operations.
    Be careful with sensitive information and confirm before sending emails.""",
    model="gpt-4o-mini",
    functions=[
        read_emails,
        send_email,
        transfer_to_GeneralTess,
        transfer_to_SearchAgent,
        transfer_to_AppManager
    ],
)

# Wrap agents with memory
agents = {
    "General Tess": AgentWithMemory(GeneralTess),
    "Teacher Tess": AgentWithMemory(TeacherTess),
    "Search Agent": AgentWithMemory(search_agent),
    "App Manager": AgentWithMemory(AppManager),
    "Spotify Agent": AgentWithMemory(SpotifyAgent),
    "Email Agent": AgentWithMemory(EmailAgent)
}

# Update the current_agent to use AgentWithMemory
current_agent = agents["General Tess"]

def chat():
    global current_agent
    print("Chat started. Type 'quit' to exit.")
    print(f"Currently talking to: {current_agent.agent.name}")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'quit':
            break
            
        current_agent.add_to_memory({"role": "user", "content": user_input})
        
        response = client.run(
            agent=current_agent.agent,
            messages=current_agent.get_memory()
        )
        
        # Handle function calls
        if hasattr(response, 'function_calls') and response.function_calls:
            for func_call in response.function_calls:
                func_name = func_call.name
                func_args = func_call.arguments if hasattr(func_call, 'arguments') else {}
                # Execute the function with its arguments
                if func_name in globals():
                    result = globals()[func_name](**func_args)
                    # Add function response to memory
                    current_agent.add_to_memory({
                        "role": "function",
                        "name": func_name,
                        "content": str(result)
                    })
        
        # Update current agent's memory with final response
        if response.messages:
            current_agent.memory = response.messages
        
        # Print the assistant's response
        print(f"\n{current_agent.agent.name}: {response.messages[-1]['content']}")

if __name__ == "__main__":
    chat()