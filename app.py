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
                 "fundstrat", "chamath"]
fridaysailer_users = ["fridaysailer"]
football_users = ["VALORANTLeaksEN", "PlayOverwatch"]

cerebro_dict = {}
fridaysailer_dict = {}
football_dict = {}

# call Screenshot class to take screenshot of webpage
econ_cal_url = "https://www.marketwatch.com/economy-politics/calendar?mod=side_nav"

# configure app timezone
def get_time():
    ny = timezone('America/New_York')
    return datetime.now(ny)


now = get_time()
last_hr = now.hour

def is_new_hr(now=get_time().hour):
    new_hr = False
    if last_hr < now:
        new_hr = True
        last_hr = get_time
    else:
        new_hr = False
    return new_hr

while True:
    # fwd every 2.5 minutes between 7am and 5pm EST every weekday
    if now.weekday() <= 4 and now.hour >= 7 and now.hour <= 17:
        # use discord webhook to send screenshot of econ calendar
        TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)
        time.sleep(60)

        # economic data is usually posted between 8:30am and 10:30am
        if is_new_hr() and now.hour <= 11:
            Screenshot(econ_cal_url, cerebro_webhook_url, "ECONOMIC CALENDAR\n").snap()

        # friday post for fridaysailer webhook
        if now.weekday() == 4 and now.hour > 8 and now.hour < 14:
            TwitterToDiscord(fridaysailer_url, fridaysailer_users, fridaysailer_dict)
            time.sleep(2.5*60)
    else:
        TwitterToDiscord(cerebro_webhook_url, cerebro_users, cerebro_dict)
        time.sleep(10*60)        
