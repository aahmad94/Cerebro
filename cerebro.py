from discord import TwitterToDiscord

with open('webhook_urls/cerebro.txt', 'r') as file:
    webhook_url = file.read().strip()
    users = ["garyblack00", "sawyermerritt", "lizannsonders", "unusual_whales", "elonmusk", "ICannot_Enough", "jpr007"]
    twitter_to_discord1 = TwitterToDiscord(webhook_url, users)