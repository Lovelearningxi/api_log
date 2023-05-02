import redis

from api_log import APILog

# 创建连接池
pool = redis.ConnectionPool(host='localhost', port=6379, password=None)

# 使用连接池创建Redis客户端
redis_client = redis.Redis(connection_pool=pool)

# 创建APILog实例
api_log = APILog()

# 设置Redis客户端
api_log.set_redis_client(redis_client)

api_log.set_table(123)
api_log.set_service('my_service')

api_log.append('/api/v1/user/123', 'GET', {'param1': 'value1', 'param2': 'value2'})
api_log.append('/api/v1/user/456', 'POST', {'param3': 'value3', 'param4': 'value4'})

logs = api_log.get_logs()
for log in logs:
    # Q:如何输出set_table名字
    print(log)

