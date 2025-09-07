**DataScope 2030**

**AI-Powered Web Evidence Finder**

DataScope 2030 is an AI-powered evidence finder that checks any news headline or article link, showing top sources and closest matches online using Retrieval-Augmented Generation (RAG) with Elastic Search and Web Search. It helps users quickly trace and verify information across the web.

---

Features

* ✅ Input a **headline** or **URL**
* ✅ Extracts the main headline from web articles
* ✅ Shows **top sources** and closest matches from the web
* ✅ Powered by **RAG (Elastic + Web Search)**
* ✅ Lightweight, futuristic, and hackathon-ready

---

## Installation (Colab)

```bash
# Install dependencies
!pip install streamlit pandas requests beautifulsoup4 pyngrok -q
```

---

## Usage (Colab)

1. Create the demo dataset (`headlines.csv`)
2. Save the Streamlit app as `app.py`
3. Run Streamlit inside Colab with Ngrok:

```python
from pyngrok import ngrok
import os
import time

# Run Streamlit in the background
os.system("nohup streamlit run app.py --server.port 8501 &")
time.sleep(5)

# Open public Ngrok URL
public_url = ngrok.connect(8501)
print("🌐 Your DataScope 2030 app is live at:", public_url)
```

4. Input a headline or URL and see top sources instantly.

---

## Security

* **Do not commit API keys** to GitHub.
* Use environment variables or a `config.py` file excluded via `.gitignore`:

```python
import os
API_KEY = os.getenv("ELASTIC_API_KEY")
```

---

## Tech Stack

* Python 3
* Streamlit (Web App)
* Pandas (Data handling)
* Requests & BeautifulSoup (Web scraping)
* Elastic Search (RAG search)
* Pyngrok (Public URL in Colab)

---

## Demo

* Input a headline or URL: e.g.,

  > “Online Hackathon | HackerEarth developer event | Forge the Future”
* Output: Extracted headline + 5 closest web sources

---

## Future Improvements

* Multi-language support
* Academic papers & PDFs integration
* Browser extension for instant verification
* Score-based credibility ranking

---

## License

MIT License
