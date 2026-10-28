import schedule
import subprocess
import time
import os

def run_focus_tracker():
    print("Running focus_tracker.py...")

    try:
        subprocess.run(
            ["python", "focus_tracker.py"],
            check=True
        )
        print("Focus tracker completed successfully.")

    except Exception as e:
        print(f"Error: {e}")


# Run once immediately
run_focus_tracker()

# Schedule every hour
schedule.every().hour.do(run_focus_tracker)

print("Hourly scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(30)  