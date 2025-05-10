import json
import os
CONFIG_PATH = "Config/config_private.json"



import json
import os
import unicodedata

CONFIG_PATH = "Config/data_table_private.json"

def normalize(text):
    return unicodedata.normalize("NFKC", text.strip())

def load_table_url(table_name: str) -> str:
    table_name = normalize(table_name)
    print(f"\n🟡 ต้องการหา: {table_name}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        print(f"🔍 เทียบกับ: {normalize(entry['table_name'])}")
        if normalize(entry["table_name"]) == table_name:
            print(f"✅ เจอ URL: {entry['redirect_url']}")
            return entry["redirect_url"]

    raise ValueError(f"❌ ไม่พบโต๊ะชื่อ: {table_name}")
