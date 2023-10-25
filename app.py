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

# configure app timezone
def get_time():
    ny = timezone('America/New_York')
    return datetime.now(ny)

sent_hr = 0
while True:
    now = get_time()
    
    if now.hour == 0 and now.minute < 10:
        sent_hr = 0

    # enter loop every hour starting at 8 AM
    if now.hour % 8 <= 4 and now.hour > sent_hr % 24:
        # send until 12 pm and at end of day at 9 pm
        if now.hour % 8 <= 4 or now.hour == 21:  
            Screenshot(cerebro_webhook_url, market_watch_snap["url"], market_watch_snap["css"], market_watch_snap["modal"], market_watch_snap["info"]).snap()    
        # send until 7 pm
        if now.hour <= 19:
            Screenshot(cerebro_webhook_url, barrons_snap["url"], barrons_snap["css"], barrons_snap["modal"], barrons_snap["info"]).snap()
        sent_hr = now.hour

    # fwd every 2.5 minutes between 7am and 5pm EST every weekday
    if now.weekday() <= 4 and now.hour >= 7 and now.hour <= 17:
        # use discord webhook to send screenshot of econ calendar
        TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)
        time.sleep(60)

        # friday post for fridaysailer webhook
        if now.weekday() == 4 and now.hour > 8 and now.hour < 14:
            TwitterToDiscord(fridaysailer_url, fridaysailer_users, fridaysailer_dict)
            time.sleep(2.5*60)
    else:
        TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)
        time.sleep(10*60)        
