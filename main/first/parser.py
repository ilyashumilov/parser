import requests
import bs4
import time
# from proxy import getips
class result:
    def __init__(self,title,price,date,url):
        self.title = title
        self.price = price
        self.date = date
        self.url = url

    def __str__(self):
        return str(self.title) + '-' + str(self.url)

class parser:
    def __init__(self,query):
        self.query = query

    def __str__(self):
        return str(self.query)

    # def __init__(self):
        # self.session = requests.Session()
        # self.session.headers = {
        #     'User Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        #     'Accept Language': 'ru',
        # }

    def page(self, page: int = None):
        payload = {
            'q': self.query
        }
        if page and page > 0:
            payload['p']:page

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

        url = 'https://www.avito.ru/sankt-peterburg/'

        # proxy = {
        #     "https": '94.73.239.124',
        # }
        # self.session.proxies.update(proxy)

        r = requests.get(url,headers=headers, params=payload)

        return r.text

    def last_page(self):
        text = self.page(page=2)
        # print(text)
        soup = bs4.BeautifulSoup(text,'lxml')
        pages = soup.select('span.pagination-item-JJq_j')
        # print(pages)

        return(pages[-2].string)

    def block(self):
        result = None
        # for i in range(int(self.last_page())+1):
        for i in range(2):
            text = self.page(page=i)
            soup=bs4.BeautifulSoup(text,'lxml')
            part = soup.select('div.iva-item-content-rejJg')
            result = []
            for i in part:
                item = self.parseblock(i)
                payload = {
                    'title':item.title,
                    'price':item.price,
                    'date':item.date,
                    'url':'https://www.avito.ru/' + str(item.url),
                }
                result.append(payload)
            time.sleep(6)

        print(result)
        return result

    def parseblock(self,block):
        # get url
        selector = 'link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH'
        link_block = block.find('a',class_=selector)
        if link_block:
            link = link_block['href']
        else:
            link = None

        # get title
        selector = 'title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO'
        title_block = block.find('h3', selector)

        if title_block:
            title = title_block.string.strip()
        else:
            title = None

        # get date
        selector = 'date-text-KmWDf text-text-LurtD text-size-s-BxGpL text-color-noaccent-P1Rfs'
        date_block = block.find('div', selector)

        if date_block:
            date = date_block.string.strip()
        else:
            date = None

        # get price
        selector = 'price-text-_YGDY text-text-LurtD text-size-s-BxGpL'

        price_block = block.find('span', selector)
        price_block = price_block.get_text('\n')

        price_block = list(filter(None,map(lambda i: i.strip(), price_block.split('\n'))))

        try:
            amount = price_block[0].replace('\xa0',' ')
            currency = price_block[1]
        except:
            amount = price_block[0]
            currency = '₽'

        price = amount + ' ' + currency

        return result(title,price,date,link)


def parse():
    p = parser('q')
    print(p.block())

if __name__ == '__main__':
    parse()

# p = parser(query='iPhone X')
#
# print(p.block())

