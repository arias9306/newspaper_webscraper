import argparse
import logging
import pandas as pd

from article import Article
from database import Base, engine, Session


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)

    args = parser.parse_args()
    filename = args.filename

    articles = pd.read_csv(filename, delimiter=';')

    Base.metadata.create_all(engine)
    postgres_session = Session()
    for index, row in articles.iterrows():
        article = Article(
            row['uid'],
            row['body'],
            row['host'],
            row['title'],
            row['newspaper_uid'],
            row['n_tokens_body'],
            row['n_tokens_title'],
            row['url'],
            row['sentiment']
        )
        postgres_session.add(article)

    postgres_session.commit()
    postgres_session.close()


main()
