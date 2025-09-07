import streamlit as st
import pandas as pd
import requests, json
from bs4 import BeautifulSoup

# -----------------------------
# Config
# -----------------------------
ELASTIC_API_KEY = "LXVadkNwa0JjTFZkODhFeEdSUlE6cG9VOEVzMVVKeF81aDhmYWc4ZWZCUQ=="
ELASTIC_ENDPOINT = "https://your-elastic-domain.us-east-1.aws.found.io/_search"

# Serper API (Google Search alternative)
SERPER_API_KEY = "92d55e3ee2491ecf07c250ed8c531b8c99d708c7"
SERPER_ENDPOINT = "https://google.serper.dev/search"

# -----------------------------
# Helper functions
# -----------------------------
def search_elastic(query):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"ApiKey {ELASTIC_API_KEY}"
    }
    payload = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["headline", "content"]
            }
        }
    }
    try:
        response = requests.get(ELASTIC_ENDPOINT, headers=headers, data=json.dumps(payload), timeout=5)
        if response.status_code == 200:
            hits = response.json().get("hits", {}).get("hits", [])
            if hits:
                top_hit = hits[0]["_source"]
                return top_hit.get("headline", ""), top_hit.get("label", "unknown"), hits[0].get("_score", 0)
    except:
        pass
    return None, None, 0

def search_serper(query):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query}
    try:
        response = requests.post(SERPER_ENDPOINT, headers=headers, json=payload)
        if response.status_code == 200:
            results = response.json().get("organic", [])
            return [r.get("title") for r in results[:5]]
    except:
        pass
    return []

def extract_text_from_url(url):
    try:
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup.title.string.strip() if soup.title else None
    except:
        return None

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="DataScope 2030", page_icon="🔍", layout="centered")
st.title("🔍 DataScope 2030")
st.write("Check if a news headline or article link is Availabel using RAG (Elastic + Web Search)!")

input_option = st.radio("Choose input type:", ["Headline", "URL"])

user_input = None
if input_option == "Headline":
    user_input = st.text_area("✍️ Enter a news headline:")
elif input_option == "URL":
    user_url = st.text_input("🌍 Enter a news article link:")
    if user_url:
        extracted_text = extract_text_from_url(user_url)
        if extracted_text:
            st.write(f"📰 Extracted Headline: *{extracted_text}*")
            user_input = extracted_text
        else:
            st.error("Couldn't extract text from URL")

if st.button("Check Data") and user_input:
    # 1. Check Elastic index
    headline, label, score = search_elastic(user_input)

    if headline:
        status = "✅ Likely True" if label == "real" else "❌ Suspicious"
        st.metric("Elastic Truth Score", f"{round(score*20,2)}%")
        st.write(f"Match found: *{headline}* → {status}")
    else:
        # 2. Fallback to Serper web search
        web_results = search_serper(user_input)
        if web_results:
            st.metric("Web Evidence Found", f"{len(web_results)} sources")
            st.write("Closest matches from web:")
            for r in web_results:
                st.caption(f"- {r}")
        else:
            st.warning("❓ Not enough info found anywhere")
def rag_check_headline(headline):
    """
    RAG-style check: use Serper API or Google Search to see if headline is supported online.
    Returns status (True/False), confidence, and top source.
    """
    import requests

    # Example: Using Serper API (replace YOUR_SERPER_API_KEY)
    API_KEY = "YOUR_SERPER_API_KEY"
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": API_KEY}
    data = {"q": headline, "num": 3}

    try:
        resp = requests.post(url, headers=headers, json=data, timeout=5)
        resp.raise_for_status()
        results = resp.json().get("organic", [])
        if results:
            top_result = results[0]
            link = top_result.get("link", "")
            snippet = top_result.get("snippet", "")
            # simple heuristic: if headline words appear in top snippet → Likely True
            match_count = sum([1 for w in headline.lower().split() if w in snippet.lower()])
            confidence = int((match_count / len(headline.split())) * 100)
            status = "✅ Likely True" if confidence > 30 else "❌ Suspicious"
            return status, confidence, link
    except:
        pass
    return "❓ Not enough info", 0, None

