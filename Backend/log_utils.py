# 📁 Backend/log_utils.py
import os
import csv
import json
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Google Sheets ===
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "../Config")
CREDENTIAL_PATH = os.path.join(CONFIG_DIR, "credentials.json")
CREDS = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIAL_PATH, SCOPE)
GS_CLIENT = gspread.authorize(CREDS)
GS_SHEET = GS_CLIENT.open("Device Logs").worksheet("Sheet1")

log_buffer = []  # 👉 Buffer สำหรับเก็บ log ชั่วคราว
LAST_SEEN_PATH = os.path.join(os.path.dirname(__file__), "../logs/last_seen.json")


def add_log_to_buffer(data: dict):
    log_buffer.append(data)
    update_last_seen(data)


def update_last_seen(data: dict):
    try:
        if os.path.exists(LAST_SEEN_PATH):
            with open(LAST_SEEN_PATH, "r", encoding="utf-8") as f:
                last_seen_data = json.load(f)
        else:
            last_seen_data = {}

        device_id = data.get("device_id")
        if not device_id:
            return

        last_seen_data[device_id] = {
            "table": data.get("table"),
            "last_event": data.get("event"),
            "last_seen": data.get("timestamp") or data.get("server_time")
        }

        with open(LAST_SEEN_PATH, "w", encoding="utf-8") as f:
            json.dump(last_seen_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Failed to update last_seen.json: {e}")


def flush_logs_to_monthly_csv():
    if not log_buffer:
        return

    now = datetime.now()
    folder = "logs"
    filename = f"{now.strftime('%Y-%m')}.csv"
    filepath = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)
    write_header = not os.path.exists(filepath)

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=log_buffer[0].keys())
        if write_header:
            writer.writeheader()
        for data in log_buffer:
            writer.writerow(data)

    log_buffer.clear()  # 👉 ล้าง buffer หลังเขียน


def flush_logs_to_google_sheet():
    for data in log_buffer:
        row = [
            data.get("device_id"),
            data.get("table"),
            data.get("event"),
            data.get("timestamp"),
            data.get("server_time"),
        ]
        GS_SHEET.append_row(row)


def is_last_day_of_month(dt: datetime) -> bool:
    tomorrow = dt + timedelta(days=1)
    return tomorrow.day == 1


def should_flush_now(dt: datetime) -> bool:
    return is_last_day_of_month(dt) and dt.strftime("%H:%M") == "21:00"


def flush_if_due():
    now = datetime.now()
    if should_flush_now(now):
        flush_logs_to_monthly_csv()
        flush_logs_to_google_sheet()
