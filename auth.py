# -*- coding: utf-8 -*-

import os
import time
import hmac
import hashlib
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), ".env"))

print "===== SAMPLE ====="

api_key = os.environ["BITFLYER_API_KEY"]
api_secret = os.environ["BITFLYER_API_SECRET"]

timestamp = datetime.now().strftime('%s')
method = "GET"
path = "/v1/getchats"

text = timestamp + method + path
print text

signature = hmac.new(str(api_secret), text, hashlib.sha256).hexdigest()
print signature

