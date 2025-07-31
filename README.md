# twitter_scraper_with_crewai
# 🐦 Twitter Scraper with CrewAI-style Insights

This project is a **Playwright-based Twitter (X) scraper** that collects tweets, likes, retweets, and timestamps from any public profile. It also includes integration for **CrewAI-style agents** to analyze the scraped tweets for patterns or insights.

---

## 📌 Features

- Scrapes tweets from any X (Twitter) profile.
- Collects:
  - Tweet text
  - Timestamp
  - Number of likes
  - Number of retweets
- Stores all data in `output.jsonl` (newline-delimited JSON format).
- Handles CAPTCHA detection and stops safely.
- CREW AI-compatible structure to plug in agents for deeper insights.

---

## 📁 Folder Structure

