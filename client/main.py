import sys
import time
import requests
import datetime
from models import (
    Status,
    SubmitJobRequest,
    SubmitJobResponse,
    ErrorResponse,
    CheckJobRequest,
    CheckJobResponse,
    EquityOptionRadarRequest,
    ResultsRequest,
    ResultsResponse,
)


if __name__ == "__main__":
    req = SubmitJobRequest(
        cob_date=datetime.date(2025, 1, 1),
        requests=[
            EquityOptionRadarRequest(identifier="ABC123", osi="XYZ789")
            for _ in range(10)
        ],
    )
    print(f"Submitting job: {req}")
    resp = requests.post("http://localhost:8888/submit_job", data=req.model_dump_json())
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
            print(f"DONE! {req.cob_date.isoformat()}")
            req = ResultsRequest(job_id=job_id)
            resp = requests.get("http://localhost:8888/result", json=req.model_dump())
            try:
                resp.raise_for_status()
            except requests.HTTPError:
                resp = ErrorResponse.model_validate_json(resp.content)
                print(resp)
                sys.exit(1)
            resp = ResultsResponse.model_validate_json(resp.content)
            print(f"radars: {[r.result for r in resp.responses]}")
            sys.exit(0)
    print("Time out after 30 seconds")
    sys.exit(1)
