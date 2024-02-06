from openai import OpenAI
import os
from parse_twitter import ParseTwitter
from datetime import datetime
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv


NOTHING = "--NOTHING--"

class TwitterToDiscord:

    def __init__(self, webhook_url, users, tweets):
        load_dotenv()        
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
            shortened = self.shorten_post(tweet_text)
            content, remainder  = shortened[0], shortened[1]

            # only fwd tweets not in dict & only after dict is initialized w/ n items
            if tweet_text and tweet_url and not self.tweets.get(tweet_url):
                # mark url as visited
                self.tweets[tweet_url] = True
                gpt_result = f"\n\n\n__ChatGPT__\n\n{self.ask_gpt(tweet_text)}"
                if NOTHING in gpt_result:
                    gpt_result = '' 
                
                if len(self.tweets) >= len(self.users):
                    self.fwd_tweet(f"{user.upper()}\n\n{content}```{gpt_result}```<{tweet_url}>")


    def shorten_post(self, text, trim_len=200):
        remainder = len(text) - trim_len
        if len(text) > trim_len:
            trimmed = f"{text[:trim_len]}... ({remainder} characters remaining)"
            return [trimmed, remainder]
        return [text, 0]


    def ask_gpt(self, tweet_text):
        prompt = f"Provide any additional context for the following tweet as concisely as you can \
                  (along with any acronyms and people mentioned if they're not obvious). If the tweet is long \
                  or over 600 characters, you may concisely summarize it. Use bullet points to structure your thoughts. \
                  If you can't quite understand the tweet or if you think no additional context is needed, \
                  respond with '{NOTHING}': \n\n"
        messages = [{"role": "user", "content": prompt + tweet_text}]
        
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_KEY"), organization="org-zeOV533K5hdpS1CFEc4Ph8Mh")
            chat = client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            print("ChatGPT API endpoint success")
        except Exception as e:
            print("\n\nChatGPT API endpoint failure\n")
            print(e)
            return ''
        return chat.choices[0].message.content
                   

    def fwd_tweet(self, content):
        # add timestamp for logs
        print(f"DATETIME: {datetime.now()}")
        print(f"CONTENT:\n {content}\n")
        DiscordWebhook(url=self.webhook_url, content=content).execute()
