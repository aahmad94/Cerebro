from chrome import ScrapeUserPage
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook

webhook_url = ""
date = datetime.now()
month = date.strftime('%b')
last_month = (date - timedelta(days=30)).strftime('%b')
users = ["fridaysailer"]

tweets = []
tweet_urls = []

with open('alfonse_webhook_url.txt', 'r') as file:
    webhook_url = file.read().strip()

for user in users:
    first = ScrapeUserPage(user, 1)
    first.initAction(first.getLastTweetAction)
    tweet = first.tweet_info["tweet"]
    tweet_url = first.tweet_info["tweet_url"]

    # dont append to our list tweets that are pinned
    if "Pinned Tweet" in first.tweet_info["tweet"]:
        second = ScrapeUserPage(user, 2)
        second.initAction(second.getLastTweetAction)
        tweet = second.tweet_info["tweet"]
        tweet_url = (second.tweet_info["tweet_url"])
    
    tweets.append(tweet)
    tweet_urls.append(tweet_url)

for i in range(len(tweets)):
    tweet = tweets[i]
    url = tweet_urls[i]

    # if posted within last few hours, tweet won't have month in header
    if month not in tweet and last_month not in tweet:
        webhook = DiscordWebhook(url=webhook_url, content=url)
        webhook.execute()