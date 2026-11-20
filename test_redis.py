
import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

try:
    print("Redis server response:", r.ping())
    r.set("test", "Hello Redis!")
    print("Stored value:", r.get("test"))

except redis.ConnectionError:
    print("Redis server is not running!")
