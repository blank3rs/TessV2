from swarm import Agent
from .base import AgentWithMemory
from ..services.search_service import search_web, open_urls
from ..services.spotify_service import spotify_play_song, spotify_current_track, spotify_create_playlist
from ..services.email_service import read_emails, send_email
from ..utils.app_manager import open_local_app, find_and_open_web_app

# Transfer functions
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

def transfer_to_SearchAgent():
    global current_agent
    print("Transferred to Search Agent")
    current_agent = agents["Search Agent"]
    return current_agent.agent

def transfer_to_AppManager():
    global current_agent
    print("Transferred to App Manager")
    current_agent = agents["App Manager"]
    return current_agent.agent

def transfer_to_SpotifyAgent():
    global current_agent
    print("Transferred to Spotify Agent")
    current_agent = agents["Spotify Agent"]
    return current_agent.agent

def transfer_to_EmailAgent():
    global current_agent
    print("Transferred to Email Agent")
    current_agent = agents["Email Agent"]
    return current_agent.agent

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

# Initialize current agent
current_agent = agents["General Tess"] 