from bs4 import BeautifulSoup
import requests
import os
import pandas as pd

def main():
    page_num = 0
    topic_urls = []
    for i in range(0, 535):
        url = 'https://censor.net/ua/theme/705/koronavirus_i_karantyn/news/page/'
        page_num = i + 1
        url_new = url + str(page_num)
        topic_urls.append(url_new)
    print(len(topic_urls))
    for i in range (0, 79):
        url = 'https://censor.net/ua/theme/700/koronavirus_iz_kytayu/page/'
        page_num = i + 1
        url_new = url + str(page_num)
        topic_urls.append(url_new)
    print(len(topic_urls))
    columns_names = 'url', 'comment', 'date', 'name', 'readers'
    df1 = pd.DataFrame(columns=columns_names)
    for url in topic_urls:
        response = requests.get(url, timeout=30)
        content = BeautifulSoup(response.content, "html.parser")
        main_div = content.find('div', attrs="curpane")
        news_sections = main_div.find_all('article', attrs="item")
        url_array = []
        for news in news_sections:
            url = news.find('h3').find('a').get('href')
            url_array.append(url)
            url_array = list(dict.fromkeys(url_array))
            for url in url_array:
                comments = scrape_text(url)
                rows = []
                for item in comments:
                    rows.append({'url': url, 'comment': item.get('comment'), 'date': item.get('date'), 'name': item.get('author_name'), 'readers': item.get('readers')})
                df1 = df1.append(rows, ignore_index=True)
                df1 = df1.drop_duplicates()
                with open ('/Users/lidiiamelnyk/Documents/comments_new.csv', 'w+', encoding = 'utf-8-sig', newline = '') as file:
                    df1.to_csv(file, sep=',', na_rep='', float_format=None,
                               columns=['url', 'comment', 'date', 'name', 'readers'],
                               header=True, index= False, index_label=None,
                               mode='a', compression='infer',
                               quoting=None, quotechar='"', line_terminator=None, chunksize=None,
                               date_format=None, doublequote=True, escapechar=None, decimal='.', errors='strict')
                    file.close()
            print("Comments count {}".format(df1['comment'].count()))


def get_comments_text(url):
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    comment_text_array = []
    next_page_url = None
    try:
        comment_section = content.find('div', id='comments')
        comments_items_array = comment_section.find_all('div', attrs='item')
        next_page_url = comment_section.find('a', attrs = 'pag_next')
        profile_url_array = []
        for comment in comments_items_array:
            com = comment.find('div', attrs='commtext comment_maxheight').get_text()
            date = comment.find('div', attrs='comminfo').find('span', attrs='time').get_text()[:10]
            profile = comment.find('span', attrs='author')
            profile_url = profile.find('a').get('href')
            profile_url_array.append(profile_url)
            profile_url_array = list(dict.fromkeys(profile_url_array))
            for profile_url in profile_url_array:
                names = get_name(profile_url)
                readers = get_readers(profile_url)
                comment_text_array.append({'comment': com, 'date': date, 'author_name': names, 'readers': readers})
    except:
        comment_text_array = []
    return comment_text_array, next_page_url


def scrape_text(url):
    comment_text_array = []
    while url is not None:
        comments, url = get_comments_text(url)
        comment_text_array = comment_text_array + comments
    return comment_text_array

def get_name(url):
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    comment_author_name_array = []
    author_profile = content.find('div', attrs='wrap')
    author_profile_main = author_profile.find('div', attrs='profile_main')
    name = author_profile_main.find('div', attrs='name').find('a').get_text() #('data-user_id')
    return name

def get_readers(url):
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    comment_author_readers_array = []
    author_profile = content.find('div', attrs='wrap')
    author_profile_main = author_profile.find('div', attrs='profile_main')
    readers = author_profile_main.find('div', attrs='fval').find('a').get_text( )
    return readers


if __name__ == '__main__':
    main()
    # while True:
    #    main()
    #    time.sleep(3600)