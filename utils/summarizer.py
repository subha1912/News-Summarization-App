import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def get_news_url(company_name):
    """Fetch the top Google News result URL for a given company."""
    search_url = f"https://news.google.com/search?q={company_name.replace(' ', '%20')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    first_news = soup.find("a", {"class": "VDXfz"})
    
    if first_news:
        news_url = "https://news.google.com" + first_news["href"][1:]  # Removing initial '.'
        return news_url
    return None

def fetch_news_content(url):
    """Extracts text content from a news article."""
    if not url:
        return "No news article found."
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    paragraphs = soup.find_all("p")
    article_text = " ".join([p.get_text() for p in paragraphs])
    
    return article_text if article_text else "No content available."

def summarize_text(text, sentence_count=3):
    """Summarize text using LSA."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    
    summary = summarizer(parser.document, sentence_count)
    return " ".join([str(sentence) for sentence in summary])

if __name__ == "__main__":
    company_name = input("Enter company name: ")  # Example: Tesla, Google, Microsoft
    
    print("\nFetching latest news...")
    news_url = get_news_url(company_name)
    
    if news_url:
        print(f"News URL: {news_url}")
        news_content = fetch_news_content(news_url)
        
        print("\nSummarizing article...\n")
        summary = summarize_text(news_content, sentence_count=3)
        print("--- Summary ---\n", summary)
    else:
        print("No news articles found for this company.")




