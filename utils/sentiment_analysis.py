from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyze sentiment of a given text and return a label.
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"
