from chrome import ScrapeUserPage
from discord_webhook import DiscordWebhook

discord_webhook_url = "https://discord.com/api/webhooks/1120842606247673976/BojjHiC2088qjANnNSBkEvI_i1Sei27B_JXKs42nsBDK4LBLzhmmYs2ohiTtjMM6Dp7H"
users = ["fridaysailer", "greg16676935420"]
tweet_urls = []

for user in users:
    pinned = False
    first = ScrapeUserPage(user, 1)
    first.initAction(first.getLastTweetAction)

    if "Pinned Tweet" not in first.tweet_info["text"]:
        tweet_urls.append(first.tweet_info["tweet_url"])
    else:
        print("----- avoiding pinned tweet -----")
        second = ScrapeUserPage(user, 2)
        second.initAction(second.getLastTweetAction)
        tweet_urls.append(second.tweet_info["tweet_url"])

print(tweet_urls)

for url in tweet_urls:
    webhook = DiscordWebhook(url=discord_webhook_url, content=url)
    webhook.execute()