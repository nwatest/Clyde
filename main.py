import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = os.getenv("status", "online")  # Default to "online" if not set
custom_status = os.getenv("custom_status", "")
usertoken = os.getenv("token")
name = os.getenv("name")
emoji_id = os.getenv("id")
anim = os.getenv("anim", "false").lower() == "true"

if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = validate.json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def onliner(token, status):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    start = json.loads(ws.recv())
    heartbeat = start["d"]["heartbeat_interval"]
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows",
            },
            "presence": {"status": status, "afk": False},
        },
        "s": None,
        "t": None,
    }
    ws.send(json.dumps(auth))
    
    emoji_data = {
        "name": name,
        "id": emoji_id,
        "animated": anim,
    } if name and emoji_id else None
    
    activities = [{
        "type": 4,
        "state": custom_status,
        "name": "Custom Status",
        "id": "custom",
        "emoji": emoji_data
    }] if custom_status else []
    
    cstatus = {
        "op": 3,
        "d": {
            "since": 0,
            "activities": activities,
            "status": status,
            "afk": False,
        },
    }
    
    print(f"Sending status update: {json.dumps(cstatus, indent=4)}")
    ws.send(json.dumps(cstatus))
    online = {"op": 1, "d": None}
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps(online))

def run_onliner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        onliner(usertoken, status)
        time.sleep(30)

keep_alive()
run_onliner()
