import requests
from fastapi import FastAPI

app = FastAPI()  # ✅ Ensure FastAPI instance exists

API_KEY = "5bd10d4617df4231979a91ca49cc4f86"  # 🔹 Replace with your NewsAPI key

def fetch_news(company):
    """Fetches the latest news articles dynamically for a given company."""
    if not API_KEY:
        return {"error": "API key is missing. Please add a valid NewsAPI key."}

    url = f"https://newsapi.org/v2/everything?q={company}&language=en&pageSize=10&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Failed to fetch news. Status Code: {response.status_code}"}

    data = response.json()
    
    if "articles" in data:
        return [{"title": article["title"], "description": article["description"], "url": article["url"]}
                for article in data["articles"][:10]]  # 🔹 Fetch **latest 10** articles
    return {"error": "No news articles found for this company."}

# ✅ FastAPI Route to Fetch News
@app.get("/news/{company}")
def get_news(company: str):
    return {"news": fetch_news(company)}

