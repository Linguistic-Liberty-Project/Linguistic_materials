import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import regex as re
topic_urls = []
i=1
import itertools
for i in range(1, (i+1)):
    url = 'https://zn.ua/theme/69/'
    page_num = i + 1
    url_new = url + 'p' + str(page_num)
    topic_urls.append(url_new)
print(len(topic_urls))
url = 'https://zn.ua/WORLD/kulturnye-osobennosti-stran-vlijajut-na-borbu-s-pandemiej-the-washington-post.html'
response = requests.get(url, timeout=30)
content = BeautifulSoup(response.content, "html.parser")

url = 'https://zn.ua/actions/comments/'
article = content.find('div', attrs="comment_block_art").find('div', attrs="comments_list").find('ul', attrs="main_comments_list")['data-absnum']
myobj = {'article': article, 'page': 1, 'typeload':1, 'comtype':1}

x = requests.post(url, data = myobj, json={"key": "value"})

json_file = x.json()
to_parse = json_file['comments']['result']['html']
content = BeautifulSoup(to_parse, "html.parser")
comment_array = []
parsed_comment = content.find('li', attrs = 'comment_item').find('span', attrs ='comment_text_block').find('span', attrs='comment_txt').get_text()

parsed_name = content.find('li', attrs = 'comment_item').find('span', attrs ='user_info_block').find('span', attrs = 'user_nickname').get_text()

