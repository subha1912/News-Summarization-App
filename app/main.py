import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable unnecessary logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  

import sys
import requests
import streamlit as st

# Ensure `utils` and `api` folders are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import required modules
from api.news_api import fetch_news  
from utils.summarizer import summarize_text
from utils.sentiment_analysis import analyze_sentiment
from utils.topic_modeling import extract_topics
from utils.hindi_tts import generate_hindi_tts

def main():
    st.title(" News Summarization & Text-to-Speech Application")

    #  User Input for Company Name
    company_name = st.text_input("Enter Company Name", "Tesla")

    if st.button("Fetch News"):
        if company_name.strip():
            news_articles = fetch_news(company_name)  # Fetch news dynamically
            
            if news_articles:
                all_summaries = []
                sentiments = []
                all_topics = []
                processed_articles = []  # Store structured articles

                #  Process each article
                for idx, article in enumerate(news_articles[:10], 1):  #  Limit to 5 articles
                    summary = summarize_text(article.get('description', 'No description available'))
                    sentiment = analyze_sentiment(summary)
                    topics = extract_topics([summary])  #  Extract real topics

                    all_summaries.append(summary)
                    sentiments.append(sentiment)
                    all_topics.extend(topics)

                    #  Store processed articles for JSON output
                    processed_articles.append({
                        "Title": article.get('title', 'No Title'),
                        "Summary": summary,
                        "Sentiment": sentiment,
                        "Topics": topics
                    })

                    #  Display Each Article
                    st.subheader(f" Article {idx}: {article.get('title', 'No Title')}")
                    st.write(f" **Summary:** {summary}")
                    st.write(f" **Sentiment:** {sentiment}")
                    st.write(f" **Topics:** {', '.join(topics) if topics else 'No topics found'}")
                    st.write(f" [Read More]({article.get('url', '#')})")
                    st.write("---")

                #  Comparative Sentiment Analysis
                sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
                for article in processed_articles:
                    sentiment_counts[article["Sentiment"]] += 1

                total_articles = len(processed_articles)
                sentiment_distribution = {
                    "Positive": round((sentiment_counts["Positive"] / total_articles) * 100, 2),
                    "Negative": round((sentiment_counts["Negative"] / total_articles) * 100, 2),
                    "Neutral": round((sentiment_counts["Neutral"] / total_articles) * 100, 2)
                } if total_articles > 0 else {"Positive": 0, "Negative": 0, "Neutral": 0}

                st.subheader(" Comparative Sentiment Score")
                st.write(f" **Positive:** {sentiment_distribution['Positive']}%")
                st.write(f" **Negative:** {sentiment_distribution['Negative']}%")
                st.write(f" **Neutral:** {sentiment_distribution['Neutral']}%")

                #  Dynamic Coverage Differences
                positive_articles = [a['Summary'] for a in processed_articles if a['Sentiment'] == "Positive"]
                negative_articles = [a['Summary'] for a in processed_articles if a['Sentiment'] == "Negative"]

                coverage_differences = {
                    "Comparison": "The news coverage presents a mix of perspectives.",
                    "Impact": "The company is portrayed differently across sources."
                }

                if positive_articles and negative_articles:
                    coverage_differences["Comparison"] = f"Some articles highlight {positive_articles[0][:100]}..., while others focus on {negative_articles[0][:100]}..."
                    coverage_differences["Impact"] = "Positive news attracts investors, whereas negative news raises concerns."

                st.subheader(" Coverage Differences")
                st.write(f"**Comparison:** {coverage_differences['Comparison']}")
                st.write(f"**Impact:** {coverage_differences['Impact']}")

                # Topic Overlap Analysis (Using Real Words)
                common_topics = list(set(all_topics))[:3]  #  Extract top 3 common topics
                unique_topics_1 = list(set(all_topics[:2]))  # Unique to first few articles
                unique_topics_2 = list(set(all_topics[2:]))  # Unique to later articles
                
                st.subheader(" Topic Overlap")
                st.write("**Common Topics Across Articles:**")
                st.write(", ".join(common_topics) if common_topics else "No common topics found")

                st.write("**Unique Topics in Initial Articles:**")
                st.write(", ".join(unique_topics_1) if unique_topics_1 else "No unique topics")

                st.write("**Unique Topics in Later Articles:**")
                st.write(", ".join(unique_topics_2) if unique_topics_2 else "No unique topics")

                #  Dynamic Final Sentiment Summary
                final_sentiment_text = f"For {company_name}, {sentiment_distribution['Positive']}% of the news is positive, {sentiment_distribution['Negative']}% is negative, and {sentiment_distribution['Neutral']}% is neutral."

                if sentiment_distribution["Positive"] > sentiment_distribution["Negative"]:
                    final_sentiment_text += " The overall sentiment leans positive, which could be beneficial for investor confidence."
                elif sentiment_distribution["Negative"] > sentiment_distribution["Positive"]:
                    final_sentiment_text += " The overall sentiment leans negative, indicating concerns about the company's performance."
                else:
                    final_sentiment_text += " The sentiment is fairly balanced, with no strong trend in either direction."

                st.subheader(" Final Sentiment Analysis")
                st.write(final_sentiment_text)

                #  Generate Hindi Speech for Sentiment Summary
                if st.button(" Play Sentiment Summary in Hindi"):
                    speech_file = generate_hindi_tts(final_sentiment_text)
                    st.audio(speech_file, format="audio/mp3")

                #  JSON Output
                final_output = {
                    "Company": company_name,
                    "Articles": processed_articles,
                    "Comparative Sentiment Score": {
                        "Sentiment Distribution": sentiment_distribution
                    },
                    "Coverage Differences": coverage_differences,
                    "Topic Overlap": {
                        "Common Topics": common_topics,
                        "Unique Topics in First Articles": unique_topics_1,
                        "Unique Topics in Later Articles": unique_topics_2
                    },
                    "Final Sentiment Analysis": final_sentiment_text
                }

                st.subheader(" JSON Output (For Reference)")
                st.json(final_output)

            else:
                st.warning(" No news articles found. Try a different company.")
        else:
            st.error(" Please enter a valid company name.")

if __name__ == "__main__":
    main()







