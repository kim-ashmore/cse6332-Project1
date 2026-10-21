"""
Kimberlee Ashmore
Project 1
Cloud Computing
"""
import json
import os
from datetime import date
from pathlib import Path

from flask import Flask, jsonify, render_template

BASE = Path(__file__).resolve().parent
IMAGES = BASE / "static" / "images"

app = Flask(__name__)
app.json.sort_keys = False


def load_photos():
    """Read photos.json on every request, so caption edits show up without a restart."""
    photos = json.loads((BASE / "photos.json").read_text(encoding="utf-8"))
    for p in photos:
        d = date.fromisoformat(p["date"])
        p["date_label"] = f"{d:%b} {d.day}, {d.year}"
        p["exists"] = (IMAGES / p["file"]).is_file()
    return sorted(photos, key=lambda p: (p["date"], p["file"]))


@app.get("/")
def index():
    photos = load_photos()
    missing = [p["file"] for p in photos if not p["exists"]]
    return render_template("index.html", photos=photos, missing=missing)


@app.get("/api/photos")
def api_photos():
    """JSON for the same data (image paths are relative to the app root)."""
    return jsonify([{**p, "url": f"static/images/{p['file']}"} for p in load_photos()])


@app.get("/healthz")
def healthz():
    return "ok\n", 200, {"Content-Type": "text/plain"}


@app.after_request
def headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    if resp.mimetype in ("image/jpeg", "image/webp", "image/png"):
        resp.headers["Cache-Control"] = "public, max-age=2592000, immutable"
    return resp


if __name__ == "__main__":
    # 0.0.0.0 so it is reachable from outside the container (course ports 9000-9009).
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 9001)), debug=bool(os.environ.get("FLASK_DEBUG")))
