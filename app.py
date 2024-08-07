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
cerebro_users = [ 
                 "KobeissiLetter", "DeItaone",
                ]
fridaysailer_users = ["fridaysailer"]
football_users = ["VALORANTLeaksEN", "PlayOverwatch"]

cerebro_dict = {}
fridaysailer_dict = {}
football_dict = {}

# arguments to instantiate Screenshot class with to be able to generate and fwd image
market_watch_snap = {
    "url": "https://tradingeconomics.com/united-states/calendar",
    "css": ".col-xl-8",
    "modal": False,
    "info": "ECONOMIC CALENDAR\n",
}

barrons_snap = {
    "url": "https://www.barrons.com/",
    "css": False,
    "modal": False,
    "info": "BARRON'S FRONT PAGE\n",
}

# configure app timezone
def get_time():
    ny = timezone('America/New_York')
    return datetime.now(ny)


def send_images(now, sent_hr):
    if now.hour > sent_hr:
        if now.hour >= 7 and now.hour <= 17 and (now.hour + 2) % 3 == 0:
            Screenshot(cerebro_webhook_url, market_watch_snap["url"], market_watch_snap["css"], market_watch_snap["modal"], market_watch_snap["info"]).snap(75) 


def fwd_tweets(now):
    # fwd every weekday between 7 am and 5 pm every minute, else fwd every 10 minutes
    if now.weekday() <= 4 and now.hour >= 7 and now.hour <= 17 and now.minute % 5 == 0:
        TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)
    elif now.minute % 10 == 0:
        TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)


sent_hr = 0
while True:
    now = get_time()
    send_images(now, sent_hr)
    fwd_tweets(now)

    if now.hour > sent_hr:
        sent_hr = now.hour % 24
    if now.hour == 0 and now.minute <= 2:
        sent_hr = 0



