import json
from dataclasses import asdict, dataclass
from uuid import uuid4

from redis import Redis

from app.config import settings


@dataclass(frozen=True)
class JobMessage:
    id: str
    job_type: str
    payload: dict


def enqueue(job_type: str, payload: dict, queue: str = "queue:default") -> JobMessage:
    message = JobMessage(id=str(uuid4()), job_type=job_type, payload=payload)
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    redis.rpush(queue, json.dumps(asdict(message), separators=(",", ":")))
    return message


def decode_job(raw: str) -> JobMessage:
    data = json.loads(raw)
    return JobMessage(id=data["id"], job_type=data["job_type"], payload=data.get("payload", {}))
