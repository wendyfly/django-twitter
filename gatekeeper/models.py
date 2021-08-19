from utils.redis_client import RedisClient

# Store those info in redis because those infos are frequently visited


class GateKeeper(object):

    @classmethod
    def get(cls, gk_name):
        conn = RedisClient.get_connection()
        # use prefix to determine the usage of rdis
        name = f'gatekeeper:{gk_name}'
        if not conn.exists(name):
            return {'percent': 0, 'description': ''}

        redis_hash = conn.hgetall(name)
        return {
            'percent': int(redis_hash.get(b'percent', 0)),
            'description': str(redis_hash.get(b'description', '')),
        }

    @classmethod
    def set_kv(cls, gk_name, key, value):
        conn = RedisClient.get_connection()
        name = f'gatekeeper:{gk_name}'
        conn.hset(name, key, value)

    @classmethod
    def is_switch_on(cls, gk_name):
        return cls.get(gk_name)['percent'] == 100

    # a method to determine whether it's in the gatekeeper
    # use module to get consistent result when increase 10% to 20%
    @classmethod
    def in_gk(cls, gk_name, user_id):
        return user_id % 100 < cls.get(gk_name)['percent']