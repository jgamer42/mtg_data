from redis import Redis
cache_db = Redis(host='localhost', port=6379, decode_responses=True)
