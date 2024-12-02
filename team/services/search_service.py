from googlesearch import search
import requests
from bs4 import BeautifulSoup
import webbrowser
from typing import List, Dict

def scrape_url(url: str) -> str:
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

def search_web(query: str) -> List[Dict[str, str]]:
    """
    Search the web using Google Search and scrape content
    """
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
            
        return content_results
    except Exception as e:
        return [{'url': '', 'content': f"Error performing search: {str(e)}"}]

def open_urls(urls=None):
    """
    Open a list of URLs in the default web browser
    Parameters:
        urls: Can be either a list of URLs, a single URL string, or a number (1-3) 
             referring to the last search results
    """
    try:
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