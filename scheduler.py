from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess


def run_pipeline():
    print("Running daily pipeline...")
    subprocess.run(["python", "run_pipeline.py"])


scheduler = BlockingScheduler()

# run every day at 03:00
scheduler.add_job(run_pipeline, "cron", hour=3, minute=0)

print("Scheduler started...")
scheduler.start()