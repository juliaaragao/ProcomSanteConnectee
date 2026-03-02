import subprocess
import sys
from pathlib import Path

# This script runs both export_data_activity.py and export_data_sensor_csv.py in parallel.

def main():
    python = sys.executable
    #create logs directory if it doesn't exist
    logs = Path("logs")
    logs.mkdir(exist_ok=True)

    # run both scripts in parallel, redirecting their outputs to separate log files
    with open(logs / "activity.log", "w") as log1, open(logs / "sensor.log", "w") as log2:
        p1 = subprocess.Popen([python, "export_data_activity.py"], stdout=log1, stderr=subprocess.STDOUT)
        p2 = subprocess.Popen([python, "export_data_sensor_csv.py"], stdout=log2, stderr=subprocess.STDOUT)
        
        # wait the processes to finish
        try:
            code1 = p1.wait()
            code2 = p2.wait()
        except KeyboardInterrupt:
            # if user interrupts, terminate both processes
            p1.terminate()
            p2.terminate()
            raise

    # check exit codes of both processes
    if code1 != 0 or code2 != 0:
        raise SystemExit(f"Falha: activity={code1}, sensor={code2}")
    
    #if it's ok, print success message
    print("Data export completed successfully.")


if __name__ == "__main__":
    main()