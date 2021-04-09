import redis
import time

class RedisConnector():

    def __init__(self, host, port = 6379):

        self.host = host
        self.port = port
        db = 0

        self.client = redis.Redis(
            host = self.host,
            port = self.port,
            db = db
        )

    def get_keys(self):
        return self.client.keys()

    def get_table(self, table_name):

        query = "{}:*".format(table_name)
        keys = self.client.keys(query) # ignore _spark schema
        data = []
        for k in keys:
            row = self.client.hgetall(k.decode())
            row = {k.decode(): v.decode() for k, v in row.items()}
            data.append(row)

        return data

    def get_wordcount(self):

        query = "wordcount:*"
        keys = self.client.keys(query) # ignore _spark schema
        data = {}
        for k in keys:
            row = self.client.hgetall(k.decode())
            row = {k.decode(): v.decode() for k, v in row.items()}
            word = k.decode().split(":")[1]

            data[word] = int(row['count'])
        
        return data


if __name__ == "__main__":
    client = RedisConnector(host = "172.17.0.2")
    data = client.get_wordcount()
    print(data)