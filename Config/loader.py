import json
import os

CONFIG_PATH = "Config/config_private.json"

def load_table_url(table_name: str) -> str:
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"❌ ไม่พบไฟล์: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        if entry["table_name"] == table_name:
            return entry["redirect_url"]

    raise ValueError(f"❌ ไม่พบโต๊ะชื่อ: {table_name}")
