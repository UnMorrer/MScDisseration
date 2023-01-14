import requests
from config import *

r = requests.get(jooble_url)
response = r.text
a = 1