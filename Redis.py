import redis
import uuid
r = redis.Redis(host="localhost", port=6379, decode_responses=True) # Connect to Redis database

LIMIT = 5   # Rate limit settings
WINDOW = 60  # seconds
script = """      
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local member = ARGV[3]

local time = redis.call('TIME')
local now = tonumber(time[1])

-- Remove requests older than the time window
redis.call('ZREMRANGEBYSCORE', key, '-inf', now - window)
-- Count requests in the current window
local count = redis.call('ZCARD', key)

if count < limit then
    -- Store the new request
    redis.call('ZADD', key, now, member)
    redis.call('EXPIRE', key, window + 1)
    return {1, count + 1, 0}
else
    -- Find the oldest request to calculate waiting time
    local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
    local wait = 0
    if oldest[2] then
        wait = math.max(1, tonumber(oldest[2]) + window - now)
    end
    return {0, count, wait}
end
"""
check_rate_limit = r.register_script(script)
def allow_request(user_id):
    key = f"rate_limit:{user_id}"
    request_id = str(uuid.uuid4())
    result = check_rate_limit(
        keys=[key],
        args=[LIMIT, WINDOW, request_id]
    )
    allowed = bool(result[0])
    count = int(result[1])
    wait_time = int(result[2])
    if allowed:
        print(f"Request ALLOWED | {user_id} | {count}/{LIMIT}")
    else:
        print(f"Request REJECTED | {user_id} | {count}/{LIMIT}")
        print(f"Try again in approximately {wait_time} seconds.")
    return allowed

user_id = "user123"    # Testing the rate limiter
for i in range(7):
    print(f"\nRequest {i + 1}:")
    allow_request(user_id)

