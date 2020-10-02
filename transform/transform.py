import argparse
import pandas as pd
import hashlib
import nltk
from urllib.parse import urlparse
from nltk.corpus import stopwords


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
    dataFrame = _remove_new_lines_from_body(dataFrame)
    dataFrame['n_tokens_title'] = _tokenize_columns(dataFrame, 'title')
    dataFrame['n_tokens_body'] = _tokenize_columns(dataFrame, 'body')
    dataFrame = _remove_duplicates(dataFrame, 'title')
    dataFrame = _remove_row_with_missing_values(dataFrame)

    _save_file(dataFrame, filename)


def _save_file(dataFrame, filename):
    new_filename = '{0}_transform.csv'.format(filename.replace('.csv', ''))
    dataFrame.to_csv(new_filename, encoding='utf-8', sep=';')


def _remove_row_with_missing_values(dataFrame):
    return dataFrame.dropna()


def _remove_duplicates(dataFrame, column):
    dataFrame.drop_duplicates(subset=[column], keep='first', inplace=True)
    return dataFrame


def _tokenize_columns(dataFrame, column):
    stop_words = set(stopwords.words('spanish'))
    return (
        dataFrame
        .dropna()
        .apply(lambda row: nltk.word_tokenize(row[column]), axis=1)
        .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
        .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
        .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
        .apply(lambda valid_words: len(valid_words))
    )


def _remove_new_lines_from_body(dataFrame):

    clean_body = (
        dataFrame
        .apply(lambda row: row['body'], axis=1)
        .apply(lambda body: list(body))
        .apply(lambda letters: list(map(lambda letter: letter.replace('\n', ''), letters)))
        .apply(lambda letters: ''.join(letters))
    )

    dataFrame['body'] = clean_body

    return dataFrame


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
