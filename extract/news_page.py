import requests
import bs4


class NewsPage:

    def __init__(self, news_site_uid, url, queries):
        self._queries = queries
        self._url = url
        self._html = None
        self._news_site_uid = news_site_uid

        self._visit(url)

    def _visit(self, url):
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')

    def _query(self, query):
        return self._html.select(query)


class HomePage(NewsPage):

    def __init__(self, news_site_uid, url, queries):
        super().__init__(news_site_uid, url, queries)

    @property
    def article_links(self):
        link_list = []
        for number in range(0, 99):
            query = self._queries['article_links'].format(number)
            for link in self._query(query):
                if link and link.has_attr('href'):
                    if link['href'].startswith('/'):
                        link_list.append(link)

        return set(link['href'] for link in link_list)


class ArticlePage(NewsPage):

    def __init__(self, news_site_uid, url, queries):
        super().__init__(news_site_uid, url, queries)

    @property
    def title(self):
        span = self._query(self._queries['article_title'])
        return span[0].text if len(span) else ''

    @property
    def body(self):
        div = self._query(self._queries['article_body'])
        return div[0].text if len(div) else ''

    @property
    def url(self):
        return self._url
