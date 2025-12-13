import sys
import time
import pydantic
from typing import Any
import requests
import datetime
from models import (
    Status,
    SubmitJobRequest,
    SubmitJobResponse,
    ErrorResponse,
    CheckJobRequest,
    CheckJobResponse,
    EquityOptionInstrument,
    ResultsRequest,
    ResultsResponse,
)
import models

def parse_response(response: requests.Response) -> Any:
    assert 'X-Message-Type' in response.headers, 'The X-Message-Type must be set on the request headers'
    response_model = getattr(models, response.headers['X-Message-Type']).model_validate_json(response.content)
    try:
        response.raise_for_status()
    except requests.RequestException as e:
        print(response_model.model_dump_json())
        raise e
    return response_model


if __name__ == "__main__":
    req = SubmitJobRequest(
        cob_date=datetime.date(2025, 1, 1),
        requests=[
            EquityOptionInstrument(identifier="ABC123", osi="XYZ789")
            for _ in range(10)
        ],
    )
    print(f"Submitting job: {req}")
    submit_job_response: SubmitJobResponse = parse_response(requests.post("http://localhost:8888/submit_job", data=req.model_dump_json()))
    job_id = submit_job_response.job_id
    for _ in range(30):
        time.sleep(1)
        print(f"Checking job status for job: {job_id}")
        check_resp: CheckJobResponse = parse_response(requests.post(
            "http://localhost:8888/check_job",
            json=CheckJobRequest(job_id=job_id).model_dump(),
        ))
        if check_resp.job.status == Status.COMPLETE:
            print(f"DONE! {req.cob_date.isoformat()}")
            req = ResultsRequest(job_id=job_id)
            result_resp: ResultsResponse = parse_response(requests.get("http://localhost:8888/results", params=req.model_dump()))
            print(f"radars: {[r.result for r in result_resp.responses]}")
            sys.exit(0)
    print("Time out after 30 seconds")
    sys.exit(1)
