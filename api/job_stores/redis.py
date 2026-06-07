from typing import Optional
from uuid import uuid4

import redis

from models import Job, Status
from api.config.job_stores.redis import RedisStoreConfig


class RedisJobStore:
    def __init__(self, config: RedisStoreConfig):
        self._prefix = config.key_prefix
        self._client = redis.Redis(
            host=config.host,
            port=config.port,
            db=config.db,
            decode_responses=True,
        )

    def _key(self, job_id: str) -> str:
        return f"{self._prefix}{job_id}"

    def add_job(self) -> Job:
        job = Job(job_id=str(uuid4()), status=Status.PENDING)
        self._client.hset(
            self._key(job.job_id),
            mapping={"job_id": job.job_id, "status": job.status.value},
        )
        return job

    def get_job(self, job_id: str) -> Job:
        data = self._client.hgetall(self._key(job_id))
        result = int(data["result"]) if data.get("result") is not None else None
        return Job(job_id=data["job_id"], status=Status(data["status"]), result=result)

    def update_job(self, job_id: str, status: Status, result: Optional[int] = None):
        mapping: dict = {"status": status.value}
        if result is not None:
            mapping["result"] = result
        self._client.hset(self._key(job_id), mapping=mapping)
