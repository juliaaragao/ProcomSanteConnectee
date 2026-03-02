import subprocess
import sys
from pathlib import Path

def main():
    python = sys.executable

    logs = Path("logs")
    logs.mkdir(exist_ok=True)

    with open(logs / "activity.log", "w") as log1, open(logs / "sensor.log", "w") as log2:
        p1 = subprocess.Popen([python, "export_data_activity.py"], stdout=log1, stderr=subprocess.STDOUT)
        p2 = subprocess.Popen([python, "export_data_sensor_csv.py"], stdout=log2, stderr=subprocess.STDOUT)

        try:
            code1 = p1.wait()
            code2 = p2.wait()
        except KeyboardInterrupt:
            # se você der Ctrl+C, mata os dois
            p1.terminate()
            p2.terminate()
            raise

    if code1 != 0 or code2 != 0:
        raise SystemExit(f"Falha: activity={code1}, sensor={code2}")

    print("Data export completed successfully.")


if __name__ == "__main__":
    main()