import json
import os
from datetime import datetime, timedelta
from log_utils import add_log_to_buffer, flush_logs_to_monthly_csv, flush_logs_to_google_sheet

LAST_SEEN_PATH = os.path.join(os.path.dirname(__file__), "../logs/last_seen.json")
LOG_FALLBACK_PATH = os.path.join(os.path.dirname(__file__), "../logs/fallback_log.csv")

def write_fallback_log(entry):
    import csv
    fieldnames = ["device_id", "table", "event", "timestamp", "server_time"]
    write_header = not os.path.exists(LOG_FALLBACK_PATH)

    with open(LOG_FALLBACK_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(entry)

def check_inactivity(timeout_minutes=60):
    if not os.path.exists(LAST_SEEN_PATH):
        print("⚠️ ไม่มีไฟล์ last_seen.json")
        return

    with open(LAST_SEEN_PATH, "r", encoding="utf-8") as f:
        last_seen_data = json.load(f)

    now = datetime.now()
    timeout_entries = []

    for device_id, info in last_seen_data.items():
        try:
            last_seen = datetime.fromisoformat(info["last_seen"])
        except Exception as e:
            print(f"❌ error parsing timestamp for {device_id}: {e}")
            continue

        if (now - last_seen) > timedelta(minutes=timeout_minutes) and info.get("last_event") not in ["leave", "timeout_leave"]:
            log_entry = {
                "device_id": device_id,
                "table": info.get("table"),
                "event": "timeout_leave",
                "timestamp": now.isoformat(),
                "server_time": now.isoformat()
            }
            add_log_to_buffer(log_entry)
            write_fallback_log(log_entry)  # ✅ fallback ไป CSV สำรองด้วย
            timeout_entries.append(log_entry)
            print(f"⏱ Timeout: {device_id} inactive > {timeout_minutes} นาที")

    if timeout_entries:
        flush_logs_to_monthly_csv()
        flush_logs_to_google_sheet()

if __name__ == "__main__":
    import schedule
    import time
    schedule.every(10).minutes.do(check_inactivity)
    print("🔁 Starting 10-minute inactivity checker...")
    while True:
        schedule.run_pending()
        time.sleep(1)
