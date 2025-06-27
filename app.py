import streamlit as st
import feedparser
from bs4 import BeautifulSoup
from PIL import Image
from datetime import datetime
import time

# --- Page Config ---
logo = Image.open("varthanow.png")
st.set_page_config(page_title="VarthaNow", page_icon=logo, layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #ffffff;
    }
    .headline:hover {
        background-color: #1f1f1f;
        box-shadow: 0 0 10px rgba(255,255,255,0.1);
        transform: scale(1.01);
    }
    .read-link {
        font-weight: bold;
        font-size: 1rem;
        color: #1e90ff;
    }
    .news-block {
        border-bottom: 1px solid #444;
        padding: 15px 0;
    }
    .source {
        color: #aaa;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Logo and Title ---
col1, col2 = st.columns([1, 10])
with col1:
    st.image(logo, width=60, use_container_width=False)
with col2:
    st.markdown("<h2 style='margin-bottom:0; color: white;'>🗞 VarthaNow</h2>", unsafe_allow_html=True)

# --- Live Time ---
time_placeholder = st.empty()

def update_time():
    while True:
        now = datetime.now().strftime("%d %B %Y, %I:%M:%S %p")
        time_placeholder.markdown(f"<p style='color:gray; text-align:right;'>🕒 Last Updated: {now}</p>", unsafe_allow_html=True)
        time.sleep(1)

# --- Search & Language Form ---
with st.form("news_form"):
    query = st.text_input("Search news...", "")
    lang = st.selectbox("Language", ["Malayalam", "English"])
    submitted = st.form_submit_button("Get News")

lang_code = "ml" if lang == "Malayalam" else "en"

# --- Clean HTML from summary ---
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

# --- Fetch News ---
def get_news(lang="ml", query=""):
    base_url = "https://news.google.com/rss"
    if query:
        url = f"{base_url}/search?q={query}&hl={lang}-IN&gl=IN&ceid=IN:{lang}"
    else:
        url = f"{base_url}?hl={lang}-IN&gl=IN&ceid=IN:{lang}"

    feed = feedparser.parse(url)
    news_items = []

    for entry in feed.entries[:10]:
        summary = clean_html(entry.summary) if "summary" in entry else ""
        source = entry.get("source", {}).get("title", "Unknown Source")
        thumbnail = entry.get("media_content", [{}])[0].get("url", "")
        news_items.append({
            "title": entry.title,
            "summary": summary,
            "link": entry.link,
            "published": entry.published,
            "source": source,
            "thumbnail": thumbnail
        })

    return news_items

# --- Show News ---
if submitted or True:  # Always show on load
    news_data = get_news(lang_code, query)
    for item in news_data:
        st.markdown(f"""
        <div class="news-block headline">
            <h5>{item['title']}</h5>
            <p>{item['summary']}</p>
            <div class="source">{item['source']} | {item['published']} 
                <a href="{item['link']}" target="_blank" class="read-link float-end">Read</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:gray;'>© 2025 | Published by Aju Krishna</div>", unsafe_allow_html=True)

# --- Run the time updater loop ---
update_time()
