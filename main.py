import requests
import certifi
from bs4 import BeautifulSoup
url = "https://timesofindia.indiatimes.com/"
path = "data/times.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "DNT": "1",  # Do Not Track
    "Referer": "https://www.google.com/",  # Mimic coming from Google
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
}

webpage=requests.get(url, HEADERS,verify=certifi.where()).text
soup = BeautifulSoup(webpage,'lxml')
captions = [fig.text.strip() for fig in soup.find_all('figcaption',class_="")]
# print(captions[0])
for cap in captions:
    print(cap, end=" |  ")
    print()
    