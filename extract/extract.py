import yaml
import argparse
import re
import news_page as news
import datetime
import csv


from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

__config = None

is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')


def configuration():
    global __config
    if not __config:
        with open('../config.yaml', mode='r') as config_file:
            __config = yaml.load(config_file, Loader=yaml.FullLoader)
    return __config


def _fetch_article(news_site_uid, url, link):
    article = None

    try:
        full_path = _build_link(url, link)
        queries = configuration()['news_sites'][news_site_uid]['queries']
        article = news.ArticlePage(news_site_uid, full_path, queries)
    except (HTTPError, MaxRetryError) as error:
        print(error)

    if article and not article.body:
        article = None

    return article


def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{0}{1}'.format(host, link)
    else:
        return '{host}{uri}'.format(uri=link, host=host)


def _save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{news_site}_{now}_articles.csv'.format(
        news_site=news_site_uid, now=now)

    csv_headers = list(
        filter(lambda property: not property.startswith('_'), dir(articles[0])))

    with open(out_file_name, mode='w+', encoding="utf-8") as articles_file:
        writer = csv.writer(articles_file)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)


def _news_scraper(news_site_uid):
    url = configuration()['news_sites'][news_site_uid]['url']
    queries = configuration()['news_sites'][news_site_uid]['queries']
    homepage = news.HomePage(news_site_uid, url, queries)

    articles = []

    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, url, link)

        if article and article.title:
            articles.append(article)

    _save_articles(news_site_uid, articles)


def main():
    parser = argparse.ArgumentParser()

    news_sites = list(configuration()['news_sites'].keys())
    parser.add_argument('news_site', help='The News site that you want to scrape',
                        type=str, choices=news_sites)

    args = parser.parse_args()

    _news_scraper(args.news_site)


main()
