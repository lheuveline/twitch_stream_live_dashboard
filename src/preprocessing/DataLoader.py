import redis
import argparse
import logging


class DataLoader:

    def __init__(self, redis_ip = "localhost"):

        self.REDIS_IP = redis_ip
        self.client = redis.Redis(self.REDIS_IP)

        self.logger = logging.getLogger(__class__.__name__)
        

    def get(self, table):

        return self.__dict__[table]

    def load_table(self, channel, table):
        
        self.keys = self.client.keys(channel + "_" + table + "*")
        self.data = [(k.decode(), self.client.hgetall(k)) for k in self.keys]

        # Add table as class property for easy access from Processor
        setattr(self, table, self.data)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("channel")
    parser.add_argument("table")
    args = parser.parse_args()

if __name__ == "__main__":
    main()