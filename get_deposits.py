# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import hmac
import hashlib
import requests
import urllib
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
from colorconsole import terminal
load_dotenv(join(dirname(__file__), ".env"))

BLACK = 0
GREEN = 2
RED = 1
LIGHT_GRAY = 7
LIGHT_CYAN = 11
WHITE = 15

screen = terminal.get_terminal(conEmu=False)
api_key = os.environ["BITFLYER_API_KEY"]
api_secret = os.environ["BITFLYER_API_SECRET"]

timestamp = str(time.time())
method = "GET"
path = "/v1/me/getdeposits"

payload = {
    "count": "30"
}

text = str.encode(timestamp + method + path + "?" + urllib.urlencode(payload))
signature = hmac.new(str(api_secret), text, hashlib.sha256).hexdigest()

url = "https://api.bitflyer.jp%s" % path
headers = {
    "ACCESS-KEY": api_key,
    "ACCESS-TIMESTAMP": timestamp,
    "ACCESS-SIGN": signature,
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers, params=payload)
json_body = response.json()
screen.clear()

for result in json_body:
    print(result)
#    if result["side"] == "BUY":
#        screen.cprint(GREEN, BLACK, "買: %s [ %s ]\n" % ("¥{:,d}".format(int(result["price"])), result["size"]))
#    elif result["side"] == "SELL":
#        screen.cprint(RED, BLACK, "売: %s [ %s ]\n" % ("¥{:,d}".format(int(result["price"])), result["size"]))
#    screen.reset()
