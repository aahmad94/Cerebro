import os
import openai
import time

from parse_twitter import ParseTwitter
from datetime import datetime
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
            parser = ParseTwitter(user)
            parser.initAction(parser.getLastTweetAction)
            
            tweet_url = parser.tweet_info["tweet_url"]
            tweet_text = parser.tweet_info["text"]

            content = f"```\n{user.upper()}\n{time.strftime('%m/%d/%Y, %H:%M')}\n{tweet_url}\n\n {tweet_text}\n```"

            # only fwd tweets not in dict & only after dict is initialized w/ n items
            if tweet_text and tweet_url and not self.tweets.get(tweet_url):
                self.tweets[tweet_url] = True
                if len(self.tweets) >= len(self.users):
                    print(datetime.now())
                    print(f"FORWARDING CONTENT -- USER: {user}")
                    self.fwd_tweet(content)
                    self.fwd_tweet(self.ask_gpt(tweet_text.lower()))


    def ask_gpt(self, tweet_text):
        prompt = "Elaborate on people mentioned in the following tweet and expand any acronyms. \
                 If any measurements or scores are mentioned, provide context around what is \
                 usually considered a good or bad measure. Use bullet points in your reply. \
                 Try to use 3 bullets and less than 325 characters. \
                 Don't summarize or rephrase the content in the tweet. Be as concise as possible. \n\n"
        messages = [{"role": "user", "content": prompt + tweet_text}]
        
        try:
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        except: 
            print("ChatGPT API endpoint failure\n")
            return ''

        return chat.choices[0].message.content
                   

    def fwd_tweet(self, content):
        print(f"CONTENT:\n {content}\n")
        DiscordWebhook(url=self.webhook_url, content=content).execute()
