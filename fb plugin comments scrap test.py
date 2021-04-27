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

topic_urls = []
i = 1

# s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s1.bind(('0.0.0.0', 80))
# s1.listen(5)

theme_url_vaccination = 'https://zn.ua/theme/14786/'
theme_url_curfew = 'https://zn.ua/theme/74/'
theme_url_corona_world = 'https://zn.ua/theme/69/'
columns_names = 'url', 'comment', 'date', 'name'


def construct_topics_urls():
    topic_urls = []
    for i in range(1, 55):
        url = theme_url_corona_world
        page_num = i + 1
        url_new = url + 'p' + str(page_num)
        topic_urls.append(url_new)
    for i in range(1, 61):
        url = theme_url_curfew
        page_num = i + 1
        url_new = url + 'p' + str(page_num)
        topic_urls.append(url_new)
    for i in range(1, 12):
        url = theme_url_vaccination
        page_num = i + 1
        url_new = url + 'p' + str(page_num)
        topic_urls.append(url_new)
    return topic_urls


def main():
    topic_urls = construct_topics_urls()
    print("Topic URLs amount {}".format(len(topic_urls)))
    url_array = []
    for url in topic_urls:
        response = requests.get(url, timeout=60)
        content = BeautifulSoup(response.content, "html.parser")
        main_div = content.find('div', attrs='sbody').find('div', id="container").find('div', id='holder').find('div',
                                                                                                                id='left')
        news_sections = None
        try:
            news_sections = main_div.find('div', attrs="left_news_list section").find('ul', attrs='news_list').find_all(
                'li')
            for news in news_sections:
                url_new = news.find('a').get('href')
                url_news = 'https://zn.ua' + url_new
                url_array.append(url_news)
                url_array = list(dict.fromkeys(url_array))
                # print("URL array length {}".format(len(url_array)))
        except AttributeError:
            print("Cannot find news_section")
            continue
    url_array = set(url_array)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for future_url in url_array:
                futures.append(executor.submit(scrape_text, url=future_url))
                for future in concurrent.futures.as_completed(futures):
                    #   time.sleep(5)
                    print(future.result())
    except:
        pass
        # for url_content in url_array:
        # scrape_text(url_content)

    # df2 = pd.read_csv('comments_new.csv', sep=',')


def request_comment(url):
    response = requests.get(url , timeout=30)
    content = BeautifulSoup(response.content, "html.parser")
    try:
        article = content.find('div', attrs="comment_block_art").find('div', attrs="comments_list").find('ul',
                                                                                                     attrs="main_comments_list")[
        'data-absnum']
        myobj = {'article': article, 'page': 1, 'typeload': 1, 'comtype': 1}
        x = requests.post(url='https://zn.ua/actions/comments/', data=myobj, headers={"Content-Type": "application/json"})
        json_file = x.json()
    except AttributeError and ValueError:
        return None
    if json_file['comments']['success']:
        return json_file
    else:
        print('No comments found here')


def get_comments_text(url):
    file = request_comment(url)
    to_parse = file['comments']['results']['html']
    content = BeautifulSoup(to_parse, "html.parser")
    comment_array = []
    parsed_comment = content.find('li', attrs='comment_item')
    try:
        for comment in parsed_comment:
            comment_text = comment.find('span', attrs='comment_text_block').find('span',
                                                                                             attrs='comment_txt').get_text()
            parsed_name = comment.find_all('span', attrs='user_info_block').find('span',
                                                                                         attrs='user_nickname').get_text()
            parsed_date = comment.find_all('span', attrs='user_info_block').find('span',
                                                                                         attrs='comment_time').get_text()
            obj = {'comment': comment_text, 'date': parsed_date, 'author_name': parsed_name}
            comment_array.append(dict(obj))
    except AttributeError:
        comment_array = []
    return comment_array, None


def scrape_text(url):
    init_url = url
    # print(init_url)
    comment_array = []
    while url is not None:
        comments, url = get_comments_text(url)
        comment_array = comment_array + comments
    rows = []
    df1 = pd.DataFrame(columns=columns_names)
    for item in comment_array:
        rows.append({'url': init_url, 'comment': item.get('comment'), 'date': item.get('date'),
                     'name': item.get('author_name')})
    df1 = df1.append(rows, ignore_index=True)
    df1 = df1.drop_duplicates()
    filename = "/Users/lidiiamelnyk/Documents/comments_folder/" + str(hash(init_url)) + '.csv'
    with open(filename, 'w+', encoding='utf-8-sig',
              newline='') as file:
        df1.to_csv(file, sep=',', na_rep='', float_format=None,
                   columns=['url', 'comment', 'date', 'name'],
                   header=True, index=False, index_label=None,
                   mode='a', compression='infer',
                   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                   date_format=None, doublequote=True, escapechar=None, decimal='.')
        print("Finished writing to {}".format(filename))
        file.close()
    count = df1['comment'].count()
    return "Comments count {}".format(count)


if __name__ == '__main__':
    main()
    # while True:
    #   main()
    #  time.sleep(120)
