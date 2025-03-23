import streamlit as st
import requests
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

def fetch_news(company_name):
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey=5bd10d4617df4231979a91ca49cc4f86"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json()["articles"]
        return articles
    return []

def summarize_text(text, max_sentences=2):
    sentences = text.split(". ")
    return ". ".join(sentences[:max_sentences]) + "."

def extract_topics(texts, num_topics=5, num_words=3):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
    X = vectorizer.fit_transform(texts)
    
    num_components = min(num_topics, X.shape[0], X.shape[1])  # Adjust for valid NMF input
    if num_components < 2:
        return ["Not enough data"]
    
    nmf = NMF(n_components=num_components, random_state=42)
    W = nmf.fit_transform(X)
    H = nmf.components_
    
    words = vectorizer.get_feature_names_out()
    topics = []
    for i in range(num_components):
        topic_words = [words[j] for j in H[i].argsort()[-num_words:]]
        topics.append(", ".join(topic_words))
    return topics

st.title("Dynamic News Summarizer")

company = st.text_input("Enter a company name:", "Tesla")

if st.button("Fetch News"):
    news_articles = fetch_news(company)
    
    if not news_articles:
        st.write("No news articles found.")
    else:
        for i, article in enumerate(news_articles[:5]):
            summary = summarize_text(article["description"] or article["content"] or "")
            topics = extract_topics([summary])

            st.subheader(f"Article {i+1}: {article['title']}")
            st.write(f"**Summary:** {summary}")
            st.write(f"**Topics:** {', '.join(topics)}")
            st.write(f"[Read More]({article['url']})")

