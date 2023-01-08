# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from tutorial.models import Quote, db_connect, create_table
import logging
import psycopg2

class SaveQuotesPipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(
            user='ukggwjdb',
            password='ynLyFB9yx_3CyG-mJ7iwDIJGzrrb8Kn6',
            host='ruby.db.elephantsql.com',
            port='',
            database='ukggwjdb'
        )
        self.cur = self.connection.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes(
            id serial PRIMARY KEY, 
            quote_content text
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute("select * from quotes where quote_content = %s", (
            item["quote_content"]
        ))
        result = self.cur.fetchone()

        if result:
            spider.logger.warn("Item already in database: %s" % item["quote_content"])

        else:
            self.cur.execute("""  insert into quotes (quote_content) values (%s) """, (
                item["quote_content"]
            ))
            self.connection.commit()

        return item

    def close_spider(self, spider):

        self.cur.close()
        self.connection.close()

class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        logging.info("****DuplicatesPipeline: database connected****")

    def process_item(self, item, spider):
        session = self.Session()
        exist_quote = session.query(Quote).filter_by(quote_content = item["quote_content"]).first()
        session.close()
        if exist_quote is not None:  # the current quote exists
            raise DropItem("Duplicate item found: %s" % item["quote_content"])
        else:
            return item