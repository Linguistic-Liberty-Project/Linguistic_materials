import bs4
from bs4 import BeautifulSoup
import requests
import os

path = os.getcwd()
#path = os.chdir('C:\\Users\\Lidiia\\OneDrive\\Documents\\PhDproject')


def main():
    page_num = 0
    topic_urls = []
    for i in range(1, 100):
        url = 'https://censor.net/ua/theme/705/koronavirus_i_karantyn/news/page/'
        page_num = i + 1
        url_new = url + str(page_num)
        topic_urls.append(url_new)
    for url in topic_urls:
        response = requests.get(url, timeout=30)
        content = BeautifulSoup(response.content, "html.parser")
        main_div = content.find('div', attrs="curpane")
        news_sections = main_div.find_all('article', attrs="item type1")
        url_array = []
        for news in news_sections:
            url = news.find('h3').find('a').get('href')
            url_array.append(url)
            url_array = list(dict.fromkeys(url_array))
            for url in url_array:
                comments = get_text(url)
                with open('/Users/lidiiamelnyk/Downloads/articles_ukrainian.txt','a', encoding = 'utf-8-sig') as myfile:
                    for row in comments:
                        myfile.write(str(row) + '\n')
                myfile.close()

def get_text(url):
    response = requests.get(url, timeout=15)
    content = BeautifulSoup(response.content, "html.parser")
    comment_text_array = []
    result = content.find('div', attrs ='text').find_all('p')
    for i in range(0, len(result)-1):
        text_section = content.find('div', attrs='text').find_all('p')[i].get_text()
        comment_text_array.append(text_section)
    return comment_text_array


if __name__ == '__main__':
    main()