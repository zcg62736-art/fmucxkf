from app.jobs import JobMessage, decode_job


def test_render_job_envelope_round_trip():
    raw = '{"id":"1","job_type":"RENDER_PAGE","payload":{"page_id":7}}'
    job = decode_job(raw)
    assert isinstance(job, JobMessage)
    assert job.job_type == "RENDER_PAGE"
    assert job.payload["page_id"] == 7
