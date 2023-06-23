from discord import TwitterToDiscord

with open('webhook_urls/fridaysailer.txt', 'r') as file:
    webhook_url = file.read().strip()
    users = ["fridaysailer"]
    twitter_to_discord2 = TwitterToDiscord(webhook_url, users)