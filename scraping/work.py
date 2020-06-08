import requests
from bs4 import BeautifulSoup
import codecs

__all__ = ('work',)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9.*/*;q=0.8'}


def work():
    url = 'http://trudbox.by/minsk?whatQuery=python'
    response = requests.get(url, headers=headers)

    jobs = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id='yw0')
        div_list = main_div.find_all('div', attrs={'class': 'row clickable'})
        for div in div_list:
            title = div.find('div', itemprop='title')
            description = div.find('div', itemprop='description')
            href = div.find_all('div', attrs={'class': 'desc'})[0].find_all('div',
                                                                            attrs={'class': 'aka_link active link'})
            if href:
                href_final = href[0]['data-href']
            else:
                href_final = 'There is no link to this vacancy, try to find it on the company site.'
            try:
                company = div.find('span', itemprop='name').text
            except AttributeError:
                company = 'Неизвестно'

            jobs.append({'title': title.text, 'description': description.text, 'url': href_final, 'company': company})

    with codecs.open('work.txt', 'w', 'utf-8') as fl:
        fl.write(str(jobs))

    return jobs


if __name__ == '__main__':
    work()
