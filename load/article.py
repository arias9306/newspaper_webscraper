from sqlalchemy import Column, String, Integer

from database import Base


class Article(Base):

    __tablename__ = 'articles'

    id = Column(String, primary_key=True)

    body = Column(String)

    host = Column(String)

    title = Column(String)

    newspaper_uid = Column(String)

    n_tokens_body = Column(Integer)

    n_tokens_title = Column(Integer)

    url = Column(String, unique=True)

    sentiment = Column(String)

    def __init__(self,
                 id,
                 body,
                 host,
                 title,
                 newspaper_uid,
                 n_tokens_body,
                 n_tokens_title,
                 url,
                 sentiment):
        self.id = id
        self.body = body
        self.host = host
        self.title = title
        self.newspaper_uid = newspaper_uid
        self.n_tokens_body = n_tokens_body
        self.n_tokens_title = n_tokens_title
        self.url = url
        self.sentiment = sentiment
