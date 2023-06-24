import time
from chrome import ParseTwitter
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook

class TwitterToDiscord:
    tweets = {}
    webhook_url = ""
    users = []

    def __init__(self, webhook_url, users, mode=1):
        self.webhook_url = webhook_url
        self.users = users
        self.get_user_tweets()

    def get_user_tweets(self):
        while True:
            for user in self.users:
                tweet = ParseTwitter(user)
                tweet.initAction(tweet.getLastTweetAction)
                tweet_text = tweet.tweet_info["tweet"]
                tweet_url = tweet.tweet_info["tweet_url"]

                if not self.tweets.get(tweet_url):
                    self.tweets[tweet_url] = True
                    print(tweet_url)
                    self.fwd_tweet(tweet_text, tweet_url)
            time.sleep(60)

    def fwd_tweet(self, tweet_text, tweet_url):
        date = datetime.now()
        month = date.strftime('%b')
        last_month = (date - timedelta(days=30)).strftime('%b')

        # if posted within last few hours, tweet won't have month in header
        if month not in tweet_text and last_month not in tweet_text:
            webhook = DiscordWebhook(url=self.webhook_url, content=tweet_url)
            webhook.execute()