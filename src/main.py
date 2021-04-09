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

    def run(self):

        while True:

            try:

                keys = self.client.keys("twitch_stream:*") # ignore _spark schema
                data = []
                for k in keys:
                    row = self.client.hgetall(k.decode())
                    row = {k.decode(): v.decode() for k, v in row.items()}
                    data.append(row)

                if len(data) == 0:
                    print('No message in timewindow !')

                for row in data:
                    print(row)

            except:
                exit(1)
            
            time.sleep(30)
            print('Batch end.')
            print('\n')


if __name__ == "__main__":
    client = RedisConnector(host = "172.17.0.2")
    client.run()