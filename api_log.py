import redis
import json
from datetime import datetime


class APILog:
    def __init__(self):
        self.redis = None
        self.table = None
        self.service = None

    def set_table(self, room_id):
        self.table = 'room:' + str(room_id)

    def set_service(self, service_name):
        self.service = service_name

    def set_redis_client(self, redis_client):
        self.redis = redis_client

    def append(self, url, method, args=None):
        if self.table is None or self.service is None:
            raise ValueError("Table and service must be set before appending logs.")

        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        log_entry = {
            'room_id': self.table,
            'service': self.service,
            'path': url,
            'method': method,
            'args': args,
            'timestamp': timestamp,
        }

        self.redis.rpush(self.table, json.dumps(log_entry))
        self.redis.expire(self.table, 86400)  # Set TTL to 24 hours (86400 seconds)

    def get_logs(self):
        if self.table is None:
            raise ValueError("Table must be set before retrieving logs.")

        logs = self.redis.lrange(self.table, 0, -1)
        return [[json.loads(log) for log in logs]]
        # 返回table名
        # return [self.table, [json.loads(log) for log in logs]]
