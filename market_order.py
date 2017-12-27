# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import hmac
import hashlib
import requests
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
from colorconsole import terminal
load_dotenv(join(dirname(__file__), ".env"))

def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

BLACK = 0
GREEN = 2
RED = 1
LIGHT_GRAY = 7
LIGHT_CYAN = 11
WHITE = 15

screen = terminal.get_terminal(conEmu=False)
argvs = sys.argv
if len(argvs) != 2:
    screen.cprint(RED, BLACK, "Please arguments: python market_order.py [+|-][size]")
    screen.reset()
    print("")
    sys.exit()

size = float(argvs[1])

side = None
side_jp = None
if size == 0:
    screen.cprint(RED, BLACK, "Size can not 0.")
    screen.reset()
    print("")
    sys.exit()
elif size < 0:
    size *= -1
    side = "SELL"
    side_jp = "売"
elif size > 0:
    size *= 1
    side = "BUY"
    side_jp = "買"

screen.reset()
screen.cprint(LIGHT_GRAY, BLACK, "Order: ")
screen.cprint(WHITE, BLACK, side_jp)
screen.reset()
print("")
screen.cprint(LIGHT_GRAY, BLACK, "Size : ")
screen.cprint(WHITE, BLACK, size)
screen.reset()
print("")

api_key = os.environ["BITFLYER_API_KEY"]
api_secret = os.environ["BITFLYER_API_SECRET"]

timestamp = str(time.time())
method = "POST"
path = "/v1/me/sendchildorder"

payload = {
    "product_code": "FX_BTC_JPY",
    "child_order_type": "MARKET",
    "side": side,
    "size": size
}

text = str.encode(timestamp + method + path + json.dumps(payload))
signature = hmac.new(str(api_secret), text, hashlib.sha256).hexdigest()

url = "https://api.bitflyer.jp%s" % path
headers = {
    "ACCESS-KEY": api_key,
    "ACCESS-TIMESTAMP": timestamp,
    "ACCESS-SIGN": signature,
    "Content-Type": "application/json"
}

if not query_yes_no("Send order?"):
    screen.cprint(GREEN, BLACK, "Canceled order.")
    sys.exit()

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.text)
