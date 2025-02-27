import requests
import certifi
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Download dependencies
nltk.download("vader_lexicon")
nltk.download("stopwords")
nltk.download("punkt")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

url = "https://timesofindia.indiatimes.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

try:
    response = requests.get(url, headers=HEADERS, verify=certifi.where())
    response.raise_for_status()
    webpage = response.text

    soup = BeautifulSoup(webpage, "lxml")
    captions = [fig.text.strip() for fig in soup.find_all("figcaption") if fig.text.strip()]

    if not captions:
        print("No captions found.")
    else:
        # Ask user for analysis type
        print("\nChoose an option:")
        print("1️⃣ Individual Captions Sentiment Analysis")
        print("2️⃣ Overall Webpage Sentiment Analysis Only")
        print("3️⃣ Keyword Extraction from Captions")
        print("4️⃣ Trending Word Cloud Visualization")
        choice = input("Enter 1, 2, 3, or 4: ").strip()

        total_sentiment = 0
        count = 0
        all_text = " ".join(captions)

        if choice == "1":
            print("\n🔹 Extracted Captions and Sentiment Analysis:\n")
            for cap in captions:
                sentiment = sia.polarity_scores(cap)
                print(f"📝 Caption: {cap}")
                print(f"👍 Positive: {sentiment['pos']:.2f}, 👎 Negative: {sentiment['neg']:.2f}, 😐 Neutral: {sentiment['neu']:.2f}")
                print(f"⚖️ Overall Sentiment Score: {sentiment['compound']:.2f}")
                print("-" * 80)

                total_sentiment += sentiment["compound"]
                count += 1

        elif choice == "3":
            # Feature 1: Keyword Extraction
            words = nltk.word_tokenize(all_text.lower())
            stopwords = set(nltk.corpus.stopwords.words("english"))
            filtered_words = [word for word in words if word.isalnum() and word not in stopwords]
            word_freq = Counter(filtered_words)

            print("\n🔹 Top 10 Most Common Words in Captions:")
            for word, freq in word_freq.most_common(10):
                print(f"🔹 {word}: {freq} times")

        elif choice == "4":
            # Feature 2: Word Cloud Visualization
            print("\n📊 Generating Word Cloud...")
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)

            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.title("Trending Words in News Captions")
            plt.show()

        # Calculate overall sentiment if not chosen
        for cap in captions:
            sentiment = sia.polarity_scores(cap)
            total_sentiment += sentiment["compound"]
            count += 1

        overall_sentiment_score = total_sentiment / count if count > 0 else 0
        overall_sentiment = (
            "Positive 😀" if overall_sentiment_score > 0.05 else
            "Negative 😠" if overall_sentiment_score < -0.05 else
            "Neutral 😐"
        )

        print("\n🔹 Overall Webpage Sentiment Analysis:")
        print(f"📊 Average Sentiment Score: {overall_sentiment_score:.2f}")
        print(f"🌍 Overall Sentiment: {overall_sentiment}")

except requests.exceptions.RequestException as e:
    print("❌ Error fetching the webpage:", e)
