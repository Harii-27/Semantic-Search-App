import requests
from bs4 import BeautifulSoup

def fetch_clean_text(url):
    """
    Fetch HTML content from URL and extract clean text.
    Returns the cleaned text or raises an exception if fetching fails.
    """
    # Better User-Agent to avoid blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    try:
        # Add timeout to prevent hanging
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises exception for bad status codes
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch URL: {str(e)}")

    html = response.text
    
    if not html or len(html.strip()) == 0:
        raise Exception("Received empty HTML content from URL")

    soup = BeautifulSoup(html, "html.parser")

    # Remove unnecessary tags
    for tag in soup(["script", "style", "noscript", "nav", "header", "footer"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    
    # Clean up extra whitespace
    text = " ".join(text.split())
    
    if not text or len(text.strip()) < 50:  # Minimum content check
        raise Exception("Insufficient text content extracted from URL (less than 50 characters)")

    return text
