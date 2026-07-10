def sync_job_status(job):

    interviews = job.interviews.all()

    if not interviews:
        job.status = "Applied"
        return

    final = next((i for i in interviews if i.is_final_round), None)

    if not final:
        job.status = "Interview"
        return

    status = final.status.lower().strip()
    result = final.result.lower().strip()

    if status != "completed":
        job.status = "Interview"
        return

    if result == "offer":
        job.status = "Offer"

    elif result == "failed":
        job.status = "Rejected"

    else:
        # passed or no response
        job.status = "Interview"