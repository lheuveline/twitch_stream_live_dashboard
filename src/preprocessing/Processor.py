import pandas as pd
import argparse
import logging
import sys

from .DataLoader import DataLoader
from .pipelines import *


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class Processor:

    def __init__(self, channel, REDIS_HOST = "localhost", redis_tables = None, redis_client = None):

        self.REDIS_HOST = REDIS_HOST
        self.channel = channel
        
        if not redis_tables:
            self.redis_tables = ["categoryCount", "wordcount", "sentiment_counts", "raw"]
        else:
            self.redis_tables = redis_tables

        # Allow to re-use previously instanciated client. If none, a new client will be instanciate using .load()
        self.redis_client = redis_client

        # NOTE : Empty sentiment counts for BFMTV records !

        self.logger = logging.getLogger(__class__.__name__)


    def __set_channel(self, channel):
        self.channel = channel

    def __get_channel(self, channel):
        return self.channel

    def __set_redis_client(self):
        self.redis_client = DataLoader(self.REDIS_HOST)

    def load(self):

        """
        Load table from enabled redis tables and expose them as class property : Processor.{table_name}
        """

        self.logger.info("Loading data for {}".format(self.channel))

        if not self.redis_client:
            self.__set_redis_client()

        for table in self.redis_tables:
            self.redis_client.load_table(self.channel, table)
            df = pd.DataFrame(self.redis_client.get(table))

            setattr(self, table, df)

    def transform(self):

        if "categoryCount" in self.redis_tables:
            self.top_categories = extract_top_categories(self.categoryCount)
            self.logger.info("Top categories pipeline : OK") # Need test

        if "wordcount" in self.redis_tables:
            self.wordcount = wordcount(self.wordcount)
            self.logger.info("Wordcount pipeline : OK") # Need test

        if "raw" in self.redis_tables:
            self.raw = get_raw_stream(self.raw)
            self.logger.info("Raw feed pipeline : OK") # Need test
        

    def run(self):

        self.load()
        self.transform()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", help = "Twitch channel to stream")
    parser.add_argument("--redis_host", help = "Redis Host")
    args = parser.parse_args()

    processor = Processor(args.channel, args.redis_host)
    processor.run()

if __name__ == "__main__":
    main()
