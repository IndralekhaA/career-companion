def sync_job_status(job):

    interviews = job.interviews.all()

    print("---- SYNC START ----")
    print("Job:", job.id)

    for i in interviews:
        print(i.status, i.result, i.is_final_round)

    if not interviews:
        job.status = "Applied"
        return

    final = next((i for i in interviews if i.is_final_round), None)

    if not final:
        job.status = "Interview"
        return

    status = final.status.lower().strip()
    result = final.result.lower().strip()



    if status == "completed":
        if result == "passed":
            job.status = "Offer"
        elif result == "rejected":
            job.status = "Rejected"
        else:
            job.status = "Interview"
    else:
        job.status = "Interview"