import platform
import subprocess
import pyautogui
import time
import webbrowser
from typing import Optional

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
        
        return f"Could not find official website for {app_name}"
    except Exception as e:
        return f"Error opening web app: {str(e)}" 