import re
import pandas as pd
import matplotlib.pyplot as plt

from googleapiclient.discovery import build
from textblob import TextBlob
from wordcloud import WordCloud


API_KEY = "API_KEY"

# https://www.youtube.com/watch?v=XXXXXXXXXXX
VIDEO_ID = "VIDEO_ID"

# Keyword untuk filtering
KEYWORD = "RUU TNI"

# Maksimal komentar yang diambil
MAX_COMMENTS = 5000

#extract video
def extract_video_id(url_or_id):
    """
    Mengambil VIDEO_ID dari YouTube URL
    atau langsung menerima VIDEO_ID.
    """
    
    if "youtube.com" in url_or_id:
        match = re.search(r"v=([^&]+)", url_or_id)
        if match:
            return match.group(1)
            
    elif "youtu.be" in url_or_id:
        match = re.search(r"youtu\.be/([^?]+)", url_or_id)
        if match:
            return match.group(1)
    
    return url_or_id


VIDEO_ID = extract_video_id(VIDEO_ID)

print("Video ID:", VIDEO_ID)

#YT API
youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

print("YouTube API connection berhasil.")

#scrape komen
def get_youtube_comments(youtube, video_id, max_comments=5000):
    
    comments = []
    next_page_token = None
    
    while len(comments) < max_comments:
        
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat="plainText"
        )
        
        response = request.execute()
        
        for item in response["items"]:
            
            comment = item["snippet"]["topLevelComment"]["snippet"]
            
            comments.append({
                "author": comment["authorDisplayName"],
                "comment": comment["textDisplay"],
                "published_at": comment["publishedAt"],
                "like_count": comment["likeCount"]
            })
            
            if len(comments) >= max_comments:
                break
        
        next_page_token = response.get("nextPageToken")
        
        if not next_page_token:
            break
    
    return pd.DataFrame(comments)

df = get_youtube_comments(
    youtube,
    VIDEO_ID,
    MAX_COMMENTS
)

print(f"Jumlah komentar: {len(df):,}")
df.head()

#data clean
def clean_text(text):
    
    text = str(text)
    
    # Lowercase
    text = text.lower()
    
    # Remove URL
    text = re.sub(r"http\S+|www\S+", "", text)
    
    # Remove mention
    text = re.sub(r"@\w+", "", text)
    
    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()

#APPLY
df["clean_comment"] = df["comment"].apply(clean_text)
df = df[df["clean_comment"].str.len() > 0].copy()

print(f"Jumlah komentar setelah cleaning: {len(df):,}")

#filter
keyword = KEYWORD.lower()

df_filtered = df[
    df["clean_comment"].str.contains(
        keyword,
        case=False,
        na=False
    )
].copy()

print(f"Komentar mengandung keyword '{KEYWORD}': {len(df_filtered):,}")

#hasil
df_filtered[
    ["comment", "published_at", "like_count"]
].head(10)

#kustom
KEYWORDS = [
    "ruu tni",
    "tni",
    "militer",
    "tentara"
]

pattern = "|".join(KEYWORDS)

df_filtered = df[
    df["clean_comment"].str.contains(
        pattern,
        case=False,
        na=False
    )
].copy()

#duplikat
before = len(df_filtered)

df_filtered = df_filtered.drop_duplicates(
    subset=["clean_comment"]
)

after = len(df_filtered)

print("Duplicate dihapus:", before - after)
print("Jumlah komentar:", after)

#spam
def detect_spam(text):
    
    text = str(text)
    
    # Terlalu banyak URL
    url_count = len(
        re.findall(r"http\S+|www\S+", text)
    )
    
    if url_count >= 2:
        return True
    
    # Komentar terlalu pendek
    if len(text.strip()) < 3:
        return True
    
    # Karakter berulang berlebihan
    if re.search(r"(.)\1{5,}", text):
        return True
    
    return False
#apply
df_filtered["is_spam"] = (
    df_filtered["comment"]
    .apply(detect_spam)
)
df_filtered = df_filtered[
    ~df_filtered["is_spam"]
].copy()

print("Jumlah komentar setelah spam filtering:", len(df_filtered))

#TEXTBLOB
def get_sentiment(text):
    
    polarity = TextBlob(text).sentiment.polarity
    
    if polarity > 0:
        sentiment = "positive"
        
    elif polarity < 0:
        sentiment = "negative"
        
    else:
        sentiment = "neutral"
    
    return pd.Series([polarity, sentiment])
#apply
df_filtered[
    ["polarity", "sentiment"]
] = df_filtered["clean_comment"].apply(
    get_sentiment
)
df_filtered[
    ["comment", "polarity", "sentiment"]
].head(10)

#sentiment distribution
sentiment_counts = (
    df_filtered["sentiment"]
    .value_counts()
)

sentiment_counts

#visualisasi
sentiment_counts.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Comments")

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#keyword analysis
from collections import Counter

all_words = " ".join(
    df_filtered["clean_comment"]
).split()

word_counts = Counter(all_words)

word_freq = pd.DataFrame(
    word_counts.items(),
    columns=["word", "frequency"]
).sort_values(
    "frequency",
    ascending=False
)

word_freq.head(20)

#wordcloud
text = " ".join(
    df_filtered["clean_comment"]
)

wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color="white",
    max_words=100
).generate(text)

plt.figure(figsize=(15, 7))

plt.imshow(
    wordcloud,
    interpolation="bilinear"
)

plt.axis("off")

plt.title("WordCloud of YouTube Comments")

plt.show()
