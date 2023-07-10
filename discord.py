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
            content = None
            if tweet_url and tweet_text:
                content = tweet_url 
                gpt_output = self.ask_gpt(tweet_text)
                if 'Nothing to add' in gpt_output:
                    content += f"\n**ChatGPT additional context:**\n{self.ask_gpt(gpt_output)}\n"
                print(content)
            else:
                print(f"Tweet URL failure for user: {user}")

            # only fwd tweets not in dict & only after dict is initialized w/ n items
            if tweet_url and content and len(tweet_text) > 5 and not self.tweets.get(tweet_url):
                self.tweets[tweet_url] = True
                if len(self.tweets) > len(self.users):
                    self.fwd_tweet(user, tweet_date, content)

    def ask_gpt(self, tweet_text):
        prompt = "Explain any not obvious acronyms or people mentioned in the following tweet, be succinct. If there's nothing to explain, reply with 'Nothing to add':\n"
        messages = [{"role": "user", "content": prompt + tweet_text}]
        try:
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        except: 
            print("ChatGPT API endpoint failure")
            return "Nothing to add"
        reply = chat.choices[0].message.content
        return reply 
                   
    def fwd_tweet(self, user, tweet_date, content):
        date = datetime.now()
        month = date.strftime('%b')
        last_month = (date - timedelta(days=30)).strftime('%b')

        # if posted within last few hours, tweet won't have month in header
        if month not in tweet_date and last_month not in tweet_date:
            print(f"FORWARDING TWEET -- user: {user}, date: {tweet_date}")
            webhook = DiscordWebhook(url=self.webhook_url, content=content)
            webhook.execute()


