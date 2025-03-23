from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_topics(texts, num_topics=2):  # Limit topics to 2 for better readability
    if not texts or all(not txt.strip() for txt in texts):
        return ["No topics found"]  # Handle empty input safely

    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)  
        X = vectorizer.fit_transform(texts)

        num_topics = min(num_topics, X.shape[0], X.shape[1])  # Ensure `n_components` is valid
        if num_topics < 1:
            return ["Insufficient data for topics"]

        nmf = NMF(n_components=num_topics, init="nndsvda", random_state=42)
        W = nmf.fit_transform(X)
        H = nmf.components_

        feature_names = vectorizer.get_feature_names_out()
        topics = [feature_names[i] for i in H[0].argsort()[-2:]]  # Pick top 2 words per topic
        return topics

    except Exception as e:
        return [f"Error: {str(e)}"]  # Return error message instead of crashing

