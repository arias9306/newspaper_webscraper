import argparse
import pandas as pd
import hashlib
from urllib.parse import urlparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='The path of the file', type=str)

    arg = parser.parse_args()
    filename = arg.filename

    dataFrame = _read_file(filename)

    news_paper_uid = _extract_news_paper_uid(filename)
    dataFrame = _add_news_paper_uid(news_paper_uid, dataFrame)
    dataFrame = _add_host_column(dataFrame)
    dataFrame = _fill_missing_titles(dataFrame)
    dataFrame = _add_uid(dataFrame)


def _add_uid(dataFrame):

    uids = (dataFrame
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
            .apply(lambda hash_: hash_.hexdigest())
            )

    dataFrame['uid'] = uids
    dataFrame.set_index('uid', inplace=True)

    return dataFrame


def _fill_missing_titles(dataFrame):

    missing_title_mask = dataFrame['title'].isna()

    missing_title = (dataFrame[missing_title_mask]['url'].str.extract(r'(?P<missing_titles>[^/]+)$')
                     .applymap(lambda title: title.split('-'))
                     .applymap(lambda title_array: ' '.join(title_array)))

    dataFrame.loc[missing_title_mask,
                  'title'] = missing_title.loc[:, 'missing_titles']

    return dataFrame


def _add_host_column(dataFrame):
    dataFrame['host'] = dataFrame['url'].apply(
        lambda url: urlparse(url).netloc)
    return dataFrame


def _add_news_paper_uid(news_paper_uid, dataFrame):
    dataFrame['newspaper_uid'] = news_paper_uid
    return dataFrame


def _extract_news_paper_uid(filename):
    return filename.split('_')[0]


def _read_file(filename):
    return pd.read_csv(filename)


main()
