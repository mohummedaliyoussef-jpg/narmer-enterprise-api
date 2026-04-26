import redis
import json
from app.config import Config

class SovereignCache:
    def __init__(self):
        self.redis = redis.from_url(Config.REDIS_URL, decode_responses=True)

    def get(self, key: str):
        try:
            data = self.redis.get(key)
            return json.loads(data) if data else None
        except:
            return None

    def set(self, key: str, value, ttl: int = 3600):
        try:
            self.redis.setex(key, ttl, json.dumps(value))
        except:
            pass
