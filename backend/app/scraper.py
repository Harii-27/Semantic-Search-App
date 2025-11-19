import requests
from bs4 import BeautifulSoup

def fetch_clean_text(url):
    # Add headers so Wikipedia, blogs, news pages allow access
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    # If failed
    if response.status_code != 200:
        return ""

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # Remove unnecessary tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text(separator=" ", strip=True)
