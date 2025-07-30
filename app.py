from config import TRACKED_LAWS
from utils.email_notify import send_email_notification
import requests, json, os

DATA_FILE = "data/last_versions.json"

def fetch_law_list(keyword):
    url = f"https://law.moj.gov.tw/api/Search.ashx?keyword={keyword}&page=1&pagesize=100"
    res = requests.get(url)
    return res.json()["Results"]

def load_last_versions():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_versions(versions):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(versions, f, ensure_ascii=False, indent=2)

def main():
    last_versions = load_last_versions()
    updated = []
    current_versions = {}

    for keyword in TRACKED_LAWS:
        for law in fetch_law_list(keyword):
            pcode = law["PCode"]
            update = law["UpdateDate"]
            title = law["Title"]
            current_versions[pcode] = update
            if last_versions.get(pcode) != update:
                updated.append(f"📘 {title}（{pcode}）已更新：{update}")

    save_versions(current_versions)

    if updated:
        send_email_notification("📢 法規查核結果", "\n".join(updated))
    else:
        print("✅ 無法規更新")

if __name__ == "__main__":
    main()
