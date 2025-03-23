#  News Summarization & Text-to-speech Application

## Project Overview  
This project extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts comparative analysis, and generates text-to-speech (TTS) output in Hindi.

### Why This Project?
Real-time News Summarization: Get the latest news articles summarized quickly.
Sentiment Analysis: Understand whether the news is **Positive, Negative, or Neutral**.
Comparative Analysis: See trends across multiple articles.
Hindi TTS (Text-to-Speech): Convert summaries into Hindi speech.
User-Friendly Web App: Uses Streamlit for a smooth UI experience.



## How It Works
### 1️⃣ News Extraction
News is fetched using `requests` from a live news API (`NewsAPI`).
Summarization is applied to reduce the content length.

### 2️⃣ Sentiment Analysis
 Uses TextBlob, a powerful NLP library.
 Classifies each article as Positive, Negative, or Neutral.

### 3️⃣ Comparative Analysis
Uses spaCy NLP to find most common keywords across articles.
Helps identify trending topics and similarities between news articles.

### 4️⃣ Hindi TTS (Text-to-Speech)
 Uses Google Text-to-Speech (gTTS).
 Converts summarized text into Hindi speech for better accessibility.




## Setup & Installation
### 1️⃣ Clone the Repository
```sh
git clone https://huggingface.co/spaces//News-Summarization
cd News-Summarization
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Backend (FastAPI)
uvicorn api.server:app --reload
Test the API: Open http://127.0.0.1:8000/docs
4️⃣ Run the Frontend (Streamlit)
streamlit run app/main.py

 Benefits & Use Cases
 Stock Market & Investment → Track sentiment on Tesla, Amazon, Google, etc.
 Media Analysis → Compare news articles from different sources.
 Public Opinion Research → Analyze people's sentiments on current events.
 Voice Accessibility → Convert important news summaries into Hindi speech for users.





