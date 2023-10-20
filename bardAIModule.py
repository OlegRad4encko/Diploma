# test of bard module

from bardapi import Bard
import os
import requests

api_key = 'cQgGKWxISF-OW-b2ODqJfuHY_nCMcK0L-32Glm3kjNKvaBAhPkjPDk_rd-dKxYDm8WslfA.'
os.environ['_BARD_API_KEY'] = api_key
token = api_key

session = requests.Session()
session.headers = {
    "Host": "bard.google.com",
    "X-Same-Domain": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://bard.google.com",
    "Referer": "https://bard.google.com/",
}
session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY"))

bard = Bard(token=token, session=session, timeout=30)

# Continued conversation without set new session
var = bard.get_answer("Коротку відповідь на питання 'Що таке земля?'")['content']

print(var)
