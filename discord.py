from chrome import ScrapeUserPage
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook

class TwitterToDiscord:
    tweets = {}
    webhook_url = ""
    users = []

    def __init__(self, webhook_url, users):
        self.webhook_url = webhook_url
        self.users = users
        self.get_user_tweets()

    def get_user_tweets(self):
        for user in self.users:
            first = ScrapeUserPage(user, 1)
            first.initAction(first.getLastTweetAction)
            tweet = first.tweet_info["tweet"]
            tweet_url = first.tweet_info["tweet_url"]

            # dont append to our list tweets that are pinned
            if "Pinned Tweet" in first.tweet_info["tweet"]:
                second = ScrapeUserPage(user, 2)
                second.initAction(second.getLastTweetAction)
                tweet = second.tweet_info["tweet"]
                tweet_url = second.tweet_info["tweet_url"]
            
            if not self.tweets.get(tweet_url):
                self.tweets[tweet_url] = True
                self.fwd_tweet(tweet, tweet_url)

    def fwd_tweet(self, tweet, tweet_url):
        date = datetime.now()
        month = date.strftime('%b')
        last_month = (date - timedelta(days=30)).strftime('%b')

        # if posted within last few hours, tweet won't have month in header
        if month not in tweet and last_month not in tweet:
            webhook = DiscordWebhook(url=self.webhook_url, content=tweet_url)
            webhook.execute()

with open('webhook_urls/fridaysailer.txt', 'r') as file:
    webhook_url = file.read().strip()
    users = ["fridaysailer"]
    twitter_to_discord1 = TwitterToDiscord(webhook_url, users)

with open('webhook_urls/cerebro.txt', 'r') as file:
    webhook_url = file.read().strip()
    users = ["garyblack00"]
    twitter_to_discord1 = TwitterToDiscord(webhook_url, users)
