import time
from redis import Redis
from app.config import settings


def main() -> None:
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    print("fmucxkf worker started", flush=True)
    while True:
        item = redis.blpop("queue:default", timeout=5)
        if item:
            _, payload = item
            print(f"job received: {payload}", flush=True)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
