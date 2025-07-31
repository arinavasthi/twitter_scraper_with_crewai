import json

def load_tweets(filepath="output.jsonl"):
    tweets = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            tweets.append(json.loads(line))
    return tweets

def summarize_tweets(tweets):
    top_tweet = max(tweets, key=lambda x: x['likes'], default={"text": "N/A", "likes": 0, "url": "#"})
    avg_likes = sum(tweet['likes'] for tweet in tweets) / len(tweets) if tweets else 0
    avg_retweets = sum(tweet['retweets'] for tweet in tweets) / len(tweets) if tweets else 0
    return {
        "total_tweets": len(tweets),
        "average_likes": round(avg_likes, 2),
        "average_retweets": round(avg_retweets, 2),
        "most_liked_tweet": top_tweet["text"],
        "most_liked_url": top_tweet["url"],
        "likes": top_tweet["likes"]
    }

if __name__ == "__main__":
    tweets = load_tweets()
    summary = summarize_tweets(tweets)
    print("Tweet Insights Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")
