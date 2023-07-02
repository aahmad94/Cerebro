from parse_twitter import ParseTwitter
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook

class TwitterToDiscord:
    tweets = None
    webhook_url = None
    users = None

    def __init__(self, webhook_url, users, tweets):
        self.tweets = tweets
        self.webhook_url = webhook_url
        self.users = users
        self.get_user_tweets()

    def get_user_tweets(self):
        for user in self.users:
            tweet = ParseTwitter(user)
            tweet.initAction(tweet.getLastTweetAction)
            
            tweet_date = tweet.tweet_info["date"]
            tweet_url = tweet.tweet_info["tweet_url"]
            tweet_text = tweet.tweet_info["text"]
            text = None
            if tweet_url:
                # temporary fix to address Twitter changes
                tweet_url = tweet_url.replace('twitter', 'vxtwitter')
                text = user + f" {tweet_date}" + \
                    "\n" + tweet_text + "\n" + tweet_url + "\n"
                print(tweet_url)

            # only fwd tweets not in dict & only after dict is initialized w/ n items
            if tweet_url and not self.tweets.get(tweet_url):
                self.tweets[tweet_url] = True
                if len(self.tweets) > len(self.users):
                    self.fwd_tweet(user, tweet_date, tweet_url)
                    
    def fwd_tweet(self, user, tweet_date, tweet_text):
        date = datetime.now()
        month = date.strftime('%b')
        last_month = (date - timedelta(days=30)).strftime('%b')

        # if posted within last few hours, tweet won't have month in header
        if month not in tweet_date and last_month not in tweet_date:
            print(f"forwarding tweet -- user: {user}, date: {tweet_date}")
            webhook = DiscordWebhook(url=self.webhook_url, content=tweet_text)
            webhook.execute()


