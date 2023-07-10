import os
import openai

from parse_twitter import ParseTwitter
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv

class TwitterToDiscord:

    def __init__(self, webhook_url, users, tweets):
        load_dotenv()
        openai.organization = "org-zeOV533K5hdpS1CFEc4Ph8Mh"
        openai.api_key = os.getenv("OPENAI_KEY")
        
        self.tweets = tweets
        self.webhook_url = webhook_url
        self.users = users
        self.get_user_tweets()

    def get_user_tweets(self):
        for user in self.users:
            tweet = ParseTwitter(user)
            tweet.initAction(tweet.getLastTweetAction)
            
            tweet_url = tweet.tweet_info["tweet_url"]
            tweet_date = tweet.tweet_info["date"]
            tweet_text = tweet.tweet_info["text"]

            # format text content to send
            gpt_content = None
            if tweet_text:
                gpt_output = self.ask_gpt(tweet_text)
                gpt_content = f"**ChatGPT additional context:** (click shaded area below)\n||{gpt_output}||\n"
                print(tweet_date)
                print(tweet_url)
                print(gpt_content)
            else:
                print(f"Tweet failure for user: {user}\n")

            # only fwd tweets not in dict & only after dict is initialized w/ n items
            if tweet_url and not self.tweets.get(tweet_url):
                self.tweets[tweet_url] = True
                if len(self.tweets) > len(self.users):
                    self.fwd_tweet(user, tweet_date, tweet_url, gpt_content)

    def ask_gpt(self, tweet_text):
        prompt = "Provide additional context for the following tweet. Explain any unfamiliar terms or acronyms. Do you think the information in the tweet is likely to influence the market? Be succinct, aim to use less than 100 words in your reply.\n\n"
        messages = [{"role": "user", "content": prompt + tweet_text}]
        try:
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        except: 
            print("ChatGPT API endpoint failure\n")
            return 'Nothing to add'
        reply = chat.choices[0].message.content
        return reply 
                   
    def fwd_tweet(self, user, tweet_date, tweet_url, gpt_content):
        date = datetime.now()
        month = date.strftime('%b')
        last_month = (date - timedelta(days=30)).strftime('%b')

        # if posted within last few hours, tweet won't have month in header
        if month not in tweet_date and last_month not in tweet_date:
            print(f"FORWARDING TWEET -- user: {user}, date: {tweet_date}")
            DiscordWebhook(url=self.webhook_url, content=tweet_url).execute()
            if (gpt_content):
                DiscordWebhook(url=self.webhook_url, content=gpt_content).execute()


