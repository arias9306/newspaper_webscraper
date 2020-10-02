from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:123456@localhost/web_scraping')

Session = sessionmaker(bind=engine)

Base = declarative_base()
