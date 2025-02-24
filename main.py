import requests
import certifi
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon if not already downloaded
nltk.download("vader_lexicon")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

url = "https://timesofindia.indiatimes.com/"
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

try:
    response = requests.get(url, headers=HEADERS, verify=certifi.where())
    response.raise_for_status()  # Check for request errors
    webpage = response.text

    soup = BeautifulSoup(webpage, "lxml")
    captions = [fig.text.strip() for fig in soup.find_all("figcaption") if fig.text.strip()]

    if captions:
        print("Extracted Captions and Sentiment Analysis:\n")
        for cap in captions:
            sentiment = sia.polarity_scores(cap)
            print(f"Caption: {cap}")
            print(f"Positive: {sentiment['pos']:.2f}, Negative: {sentiment['neg']:.2f}, Neutral: {sentiment['neu']:.2f}")
            print(f"Overall Sentiment Score: {sentiment['compound']:.2f} (Positive if > 0.05, Negative if < -0.05, Neutral otherwise)")
            print("-" * 80)
    else:
        print("No captions found.")

except requests.exceptions.RequestException as e:
    print("Error fetching the webpage:", e)
