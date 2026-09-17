import time

from redis import Redis

from app.config import settings
from app.jobs import decode_job


def dispatch(job_type: str, payload: dict) -> None:
    if job_type == "PING":
        print(f"worker ping: {payload}", flush=True)
        return
    print(f"unsupported job type: {job_type}", flush=True)


def main() -> None:
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    print("fmucxkf worker started", flush=True)
    while True:
        item = redis.blpop("queue:default", timeout=5)
        if item:
            _, raw = item
            try:
                job = decode_job(raw)
                dispatch(job.job_type, job.payload)
            except Exception as exc:
                print(f"job failed: {exc}", flush=True)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
