import concurrent.futures
import json

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import socket
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from time import sleep
from random import randint

url = 'https://korrespondent.net/ukraine/politics/4351221-pochemu-rossyia-obiavyla-ob-otvode-voisk-ot-ukrayny'

response = requests.get(url, timeout=30)
content = BeautifulSoup(response.content, "html.parser")
comment_section = content.find('div', attrs = 'layout').find('div', attrs = 'layout-middle').find('div', attrs = 'layout-content').find('div', attrs = 'cols clearfix')
comments = comment_section.find('div', attrs = 'comments').find('div', attrs = 'comments_list').find('div', attrs = 'comment-item__text').get_text()
