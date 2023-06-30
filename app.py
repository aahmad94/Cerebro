import time

from discord import TwitterToDiscord

with open('assets/webhook_urls.txt', 'r') as file:
    file_contents = file.read()

# get webhook urls, define users, init TwitterToDiscord instances w/ respective args
cerebro_index = file_contents.find('cerebro_url=')
football_index = file_contents.find('football_url=')
fridaysailer_index = file_contents.find('fridaysailer_url=')

cerebro_webhook_url = file_contents[cerebro_index + len('cerebro_url='):].split('\n', 1)[0]
football_webhook_url = file_contents[football_index + len('football_url='):].split('\n', 1)[0]
fridaysailer_url = file_contents[fridaysailer_index + len('fridaysailer_url='):].split('\n', 1)[0]

# ToDo: create API endpoint to modify users list
# ToDo: change 'users' terminology (maybe Tweeters)
cerebro_users = ["FirstSquawk", "wholemarsblog", "garyblack00", "sawyermerritt", "lizannsonders",
                 "unusual_whales", "elonmusk", "ICannot_Enough", "jpr007", "troyteslike", "marionawfal"]
fridaysailer_users = ["fridaysailer"]
football_users = ["VALORANTLeaksEN", "PlayOverwatch"]

cerebro_dict = {}
fridaysailer_dict = {}
football_dict = {}

while True:
    cerebro = TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)
    fridaysailer = TwitterToDiscord(cerebro_webhook_url, fridaysailer_users, fridaysailer_dict)
    football = TwitterToDiscord(football_webhook_url, football_users, football_dict)
    time.sleep(60)


