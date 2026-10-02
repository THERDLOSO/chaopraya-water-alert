import json
import os
import requests
import config

STATE_FILE = "data/last_state.json"

def get_water_level():
    return 2.15

def send_line_notification(message, token):
    if not token or token == "YOUR_LINE_TOKEN_HERE":
        print("LINE Token not set, skipping notification.")
        return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_level": 0.0}

def save_state(level):
    os.makedirs("data", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"last_level": level}, f)

def main():
    current_level = get_water_level()
    state = load_last_state()
    last_level = state.get("last_level", 0.0)

    print(f"Current water level: {current_level} m.")

    if current_level >= 2.0 and current_level != last_level:
        msg = f"⚠️ แจ้งเตือนระดับน้ำเจ้าพระยา! ขณะนี้อยู่ที่ {current_level} เมตร (สูงกว่าเกณฑ์)"
        send_line_notification(msg, config.LINE_TOKEN)

    save_state(current_level)

if __name__ == "__main__":
    main()
