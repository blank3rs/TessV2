# Assistant v2

A modular AI assistant system with specialized agents for different tasks.

## Features

- General Assistant (GeneralTess)
- Educational Assistant (TeacherTess)
- Web Search Agent
- App Manager for opening local and web applications
- Spotify Integration
- Email Management (Gmail and Outlook)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   AZURE_OPENAI_KEY=your_key_here
   AZURE_OPENAI_VERSION=your_version_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri
   
   GMAIL_ADDRESS=your_gmail_address
   GMAIL_PASSWORD=your_gmail_app_password
   
   OUTLOOK_ADDRESS=your_outlook_address
   OUTLOOK_PASSWORD=your_outlook_app_password
   ```

## Usage

Run the assistant:
```bash
python -m team
```

The assistant will start in chat mode with GeneralTess as the default agent. You can:
- Chat naturally with the assistant
- Ask it to search the web
- Control Spotify playback
- Open applications
- Manage emails
- Get educational help

Type 'quit' to exit the chat.

## Project Structure

```
team/
├── __init__.py
├── main.py
├── agents/
│   ├── __init__.py
│   ├── base.py
│   └── agent_definitions.py
├── services/
│   ├── __init__.py
│   ├── spotify_service.py
│   ├── email_service.py
│   └── search_service.py
└── utils/
    ├── __init__.py
    └── app_manager.py
```

## Security Notes

- Use app-specific passwords for email services
- Store sensitive credentials in the `.env` file
- Never commit the `.env` file to version control 