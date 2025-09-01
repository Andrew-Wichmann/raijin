import sys
import time
import requests
from models import (
    Status,
    SubmitJobRequest,
    SubmitJobResponse,
    ErrorResponse,
    CheckJobRequest,
    CheckJobResponse,
)


if __name__ == "__main__":
    req = SubmitJobRequest(x=1, y=1)
    print(f"Submitting job: {req}")
    resp = requests.post("http://localhost:8888/submit_job", json=req.model_dump())
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        resp = ErrorResponse.model_validate_json(resp.content)
        print(resp)
        sys.exit(1)
    job_id = SubmitJobResponse.model_validate_json(resp.content).job_id
    for _ in range(30):
        time.sleep(1)
        print(f"Checking job status for job: {job_id}")
        resp = requests.post(
            "http://localhost:8888/check_job",
            json=CheckJobRequest(job_id=job_id).model_dump(),
        )
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            resp = ErrorResponse.model_validate_json(resp.content)
            print(resp)
            sys.exit(1)
        resp = CheckJobResponse.model_validate_json(resp.content)
        if resp.job.status == Status.COMPLETE:
            print(f"DONE! {req.x} + {req.y} = {resp.job.result}")
            sys.exit(0)
    print("Time out after 30 seconds")
    sys.exit(1)
