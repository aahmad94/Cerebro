from chrome import ScrapeUserPage

users = ["wholemarsblog", "SawyerMerritt"]
text = ""
for user in users:
    scraper = ScrapeUserPage(user, 1)
    scraper.initAction(scraper.getLastTweetURLAction)
    text = scraper.tweet_info["text"]

    if "Pinned Tweet" in text:
        second = ScrapeUserPage(user, 2)
        second.initAction(second.getLastTweetURLAction)
        text = second.tweet_info["text"]
        
    print(text)
    print("\n")
