import time
from datetime import datetime
from pytz import timezone


from discord import TwitterToDiscord

with open('assets/credentials.txt', 'r') as file:
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
cerebro_users = ["garyblack00", "lizannsonders", "jpr007", "SawyerMerritt",
                 "unusual_whales", "StockMKTNewz", "LiveSquawk"]
fridaysailer_users = ["fridaysailer"]
football_users = ["VALORANTLeaksEN", "PlayOverwatch"]

cerebro_dict = {}
fridaysailer_dict = {}
football_dict = {}



while True:
    ny = timezone('America/New_York')
    now = datetime.now(ny)

    if now.weekday() < 5 and now.hour > 8 and now.hour < 16:
        TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)
        if now.weekday() == 4 and now.hour > 8 and now.hour < 13:
            TwitterToDiscord(fridaysailer_url, fridaysailer_users, fridaysailer_dict)
        time.sleep(2.5*60)
    else:
        TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)
        time.sleep(20*60)        
        

        



