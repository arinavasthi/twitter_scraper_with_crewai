import asyncio
import json
import re
from playwright.async_api import async_playwright

TWEET_ARTICLE_SELECTOR = 'article[data-testid="tweet"]'
TEXT_SELECTOR = '[data-testid="tweetText"]'
LIKE_SELECTOR = '[data-testid="like"]'
RETWEET_SELECTOR = '[data-testid="retweet"]'
TIMESTAMP_SELECTOR = 'a[aria-label*="ago"] time'

def parse_count(text):
    if not text:
        return 0
    num = re.search(r'[\d,.]+', text)
    if num:
        value = num.group().replace(',', '')
        if 'K' in text:
            return int(float(value) * 1000)
        elif 'M' in text:
            return int(float(value) * 1000000)
        return int(float(value))
    return 0

async def run_scraper(profile_url: str):
    scraped_tweets_count = 0
    seen_tweet_links = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state="auth.json")
        page = await context.new_page()

        print(f"Navigating to {profile_url}...")
        try:
            await page.goto(profile_url)
            await page.wait_for_selector(TWEET_ARTICLE_SELECTOR, timeout=15000)
            print("Profile page loaded. Starting scrape...")
        except Exception as e:
            print(f"Could not load the profile page. Error: {e}")
            await browser.close()
            return

        scroll_attempts_with_no_new_tweets = 0
        with open("output.jsonl", "w", encoding="utf-8") as f:
            pass

        while scroll_attempts_with_no_new_tweets < 4:
            if await page.query_selector('text="Verify you are human"'):
                print("CAPTCHA detected. Stopping script.")
                break

            tweet_elements = await page.query_selector_all(TWEET_ARTICLE_SELECTOR)
            new_tweets_found_this_pass = False

            for tweet_element in tweet_elements:
                try:
                    timestamp_element = await tweet_element.query_selector(TIMESTAMP_SELECTOR)
                    if not timestamp_element:
                        continue
                    parent_link_element = await timestamp_element.query_selector('xpath=..')
                    tweet_link_href = await parent_link_element.get_attribute('href') if parent_link_element else None
                    if not tweet_link_href:
                        continue
                    tweet_id = tweet_link_href.split('/')[-1]
                    if tweet_id not in seen_tweet_links:
                        new_tweets_found_this_pass = True
                        seen_tweet_links.add(tweet_id)
                        text_element = await tweet_element.query_selector(TEXT_SELECTOR)
                        tweet_text = await text_element.inner_text() if text_element else ""
                        like_element = await tweet_element.query_selector(LIKE_SELECTOR)
                        like_text = await like_element.get_attribute("aria-label") if like_element else "0"
                        like_count = parse_count(like_text)
                        retweet_element = await tweet_element.query_selector(RETWEET_SELECTOR)
                        retweet_text = await retweet_element.get_attribute("aria-label") if retweet_element else "0"
                        retweet_count = parse_count(retweet_text)
                        timestamp = await timestamp_element.get_attribute('datetime')
                        tweet_data = {
                            "id": tweet_id,
                            "url": f"https://x.com{tweet_link_href}",
                            "timestamp": timestamp,
                            "text": tweet_text.strip(),
                            "likes": like_count,
                            "retweets": retweet_count,
                        }
                        with open("output.jsonl", "a", encoding="utf-8") as f:
                            f.write(json.dumps(tweet_data) + "\n")
                        scraped_tweets_count += 1
                        print(f"Scraped {scraped_tweets_count} tweets...", end='\r')
                except Exception as e:
                    print(f"\n[!] Skipping a tweet due to error: {e}")
                    pass

            if new_tweets_found_this_pass:
                scroll_attempts_with_no_new_tweets = 0
            else:
                scroll_attempts_with_no_new_tweets += 1
                print(f"\nNo new tweets found on this scroll. Attempt #{scroll_attempts_with_no_new_tweets}")

            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2.5)

        print(f"\nScraping complete. Total unique tweets saved: {scraped_tweets_count}")
        await browser.close()

if __name__ == "__main__":
    target_url = "https://x.com/AvasthiArin"  # Replace with the actual profile URL
    asyncio.run(run_scraper(target_url))
