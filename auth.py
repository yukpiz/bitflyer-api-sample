# -*- coding: utf-8 -*-

import os
import time
import hmac
import hashlib
import requests
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), ".env"))

print "===== SAMPLE ====="

api_key = os.environ["BITFLYER_API_KEY"]
api_secret = os.environ["BITFLYER_API_SECRET"]

timestamp = datetime.now().strftime('%s')
method = "GET"

text = timestamp + method
print text

signature = hmac.new(str(api_secret), text, hashlib.sha256).hexdigest()
print signature

#url = "https://api.bitflyer.jp/v1/markets"
#headers = {
#    'ACCESS-KEY': api_key,
#    'ACCESS-TIMESTAMP': timestamp,
#    'ACCESS-SIGN': signature
#}
#response = requests.get(url, headers=headers)
#print(response.json())
#
#url = "https://api.bitflyer.jp/v1/board"
#payload = {
#    'product_code': 'FX_BTC_JPY'
#}
#response = requests.get(url, headers=headers, params=payload)
#print(response.text)



