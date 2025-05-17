from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import subprocess
import json

app = FastAPI()

with open("jtv_config.json", "r") as f:
    config = json.load(f)

USERNAME = "Prajwal_07"
PASSWORD = "Prajwal_07"

@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "JioTV M3U Server is running."

@app.get("/playlist.m3u", response_class=PlainTextResponse)
def get_playlist(request: Request):
    user = request.query_params.get("u")
    pw = request.query_params.get("p")

    if user != USERNAME or pw != PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = subprocess.run(
        ["python3", "jiotv.py", "--config", "jtv_config.json", "--output", "playlist.m3u"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail="Playlist generation failed.")

    with open("playlist.m3u", "r") as f:
        return f.read()
