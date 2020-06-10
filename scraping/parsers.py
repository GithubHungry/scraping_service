import requests
from bs4 import BeautifulSoup
from random import randint
import codecs

__all__ = ('trudbox', 'work',)

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def work(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_lst:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language, })
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def trudbox(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            main_div = soup.find('div', id='yw0')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'row clickable'})
                for div in div_list:
                    title = div.find('div', itemprop='title')
                    description = div.find('div', itemprop='description')
                    href = div.find_all('div', attrs={'class': 'desc'})[0].find_all('div', attrs={
                        'class': 'aka_link active link'})
                    if href:
                        href_final = href[0]['data-href']
                    else:
                        href_final = 'There is no link to this vacancy, try to find it on the company site.'
                    try:
                        company = div.find('span', itemprop='name').text
                    except AttributeError:
                        company = 'Неизвестно'
                    jobs.append({'title': title.text, 'url': href_final,
                                 'description': description.text, 'company': company,
                                 'city_id': city, 'language_id': language,
                                 })
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


if __name__ == '__main__':
    url = 'http://trudbox.by/minsk?whatQuery=python'
    jobs, errors = trudbox(url)
    with codecs.open('work.json', 'w', 'utf-8') as fl:
        fl.write(str(jobs))
