import time
from datetime import datetime
from pytz import timezone

from discord import TwitterToDiscord
from screenshot import Screenshot

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
cerebro_users = ["garyblack00", "FredaDuan",
                 "lizannsonders", "SawyerMerritt", 
                 "KobeissiLetter", "friedberg", 
                 "fundstrat", "chamath",
                 "firstsquawk"]
fridaysailer_users = ["fridaysailer"]
football_users = ["VALORANTLeaksEN", "PlayOverwatch"]

cerebro_dict = {}
fridaysailer_dict = {}
football_dict = {}

# arguments to instantiate Screenshot class with to be able to generate and fwd image
market_watch_snap = {
    "url": "https://www.marketwatch.com/economy-politics/calendar?mod=side_nav",
    "css": ".element--textblock",
    "modal": True,
    "info": "ECONOMIC CALENDAR\n",
}

barrons_snap = {
    "url": "https://www.barrons.com/",
    "css": False,
    "modal": False,
    "info": "BARRON'S FRONT PAGE\n",
}

sent_hr = 0
sent_minute = 0

# configure app timezone
def get_time():
    ny = timezone('America/New_York')
    return datetime.now(ny)


def send_images(now, sent_hr):
    # send every hour
    if now.hour > sent_hr:
        # send until 12 pm and at end of day at 9 pm
        if now.hour % 8 <= 4 or now.hour == 21:  
            Screenshot(cerebro_webhook_url, market_watch_snap["url"], market_watch_snap["css"], market_watch_snap["modal"], market_watch_snap["info"]).snap()    
    
    # send every 2 hours
    if now.hour > sent_hr + 1:
        # send until end of day at 9 pm
        if now.hour <= 19:
            Screenshot(cerebro_webhook_url, barrons_snap["url"], barrons_snap["css"], barrons_snap["modal"], barrons_snap["info"]).snap()


def fwd_tweets(now, sent_minute):
    # fwd every weekday betweent 7 am and 5 pm every minute, else fwd every 10 minutes
    if now.weekday() <= 4 and now.hour >= 7 and now.hour <= 17 and now.minute > sent_minute + 1:
        TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)
    elif now.weekday > 4 and now.minute % 10 == 0:
        TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)        

    # friday post for fridaysailer webhook, between 8 am and 2 pm every 10 minutes
    if now.weekday() == 4 and now.hour > 8 and now.hour < 14 and now.minute % 10 == 0:
        TwitterToDiscord(fridaysailer_url, fridaysailer_users, fridaysailer_dict)
    

while True:
    now = get_time()
    if now.hour == 0 and now.minute < 10:
        sent_hr = 0
    if now.minute == 0:
        sent_minute = 0

    send_images(now, sent_hr)
    fwd_tweets(now, sent_minute)

    if now.hour > sent_hr:
        sent_hr = now.hour
    if now.minute > sent_minute:
        sent_minute = now.minute


