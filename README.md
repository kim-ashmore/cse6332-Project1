# Lapse Gallery (Flask)

Ll


```
app.py            Flask app (routes: /, /api/photos, /healthz)
photos.json       file name, date, title, caption, alt text for each photo  <- edit captions here
templates/        index.html (Jinja)
static/           style.css, gallery.js, images/  <- put your JPGs here
Dockerfile, docker-compose.yml   standalone container + Cloudflare tunnel
tools/convert_images.py          HEIC -> JPG helper
```

## 0. Add the images (not included in the zip)
Browsers can't show HEIC, so convert first (needs `pip install pillow pillow-heif`):
```bash
python tools/convert_images.py /path/to/your/heic/folder     # writes static/images/lapse_*.jpg
```
Keep the file names: they must match `photos.json`. Until the images exist, the page shows a notice saying so.

## A. Run inside the course container (Projects 1-5 image)
Copy the **contents** of this folder into `data/flask/` (replace the starter `app.py`):
```
data/flask/app.py  photos.json  templates/  static/  requirements.txt
```
- Gunicorn runs with `--reload`, so it picks up the new `app.py` by itself.
  Open **http://localhost:8080/flask/** (keep the trailing slash).
- Caption edits in `photos.json` show on refresh with no restart.
- Alternative, own port: `docker exec -d cse6332-course python3 /data/flask/app.py`
  then open http://localhost:9001 (the app listens on 0.0.0.0:9001; set `PORT` to use 9000-9009).

Public Cloudflare link for it (run on your computer, needs [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)):
```bash
cloudflared tunnel --url http://localhost:9001     # option 1: only the gallery (use the port-9001 method above)
cloudflared tunnel --url http://localhost:8080     # option 2: the whole course site; gallery at <link>/flask/
```
Prefer option 1: option 2 makes everything nginx serves public (including `/node/`).
The link is temporary and only lives while the tunnel and container run. MySQL and Redis are never exposed by either command.

## B. Standalone container
```bash
docker compose up --build
```
- Local: http://localhost:8080
- Public Cloudflare link: `docker compose logs tunnel | grep trycloudflare.com`
- Without the tunnel: `docker build -t lapse-flask . && docker run -p 8080:8000 lapse-flask`

For a link that stays up, create a named tunnel in the Cloudflare dashboard (Zero Trust > Networks > Tunnels), then change the
tunnel service command in `docker-compose.yml` to `tunnel --no-autoupdate run --token <YOUR_TOKEN>` and point a hostname at `http://web:8000`.
Keep the token out of git.

## Plain Python
```bash
pip install -r requirements.txt
python app.py          # http://localhost:9001
```

## Design notes (for the demo)
- **Relative URLs** (`static/style.css`, not `/static/...`): the same code works at `/` and behind nginx at `/flask/`.
- **Data-driven**: one Jinja loop and one JSON file instead of 12 hand-written blocks; the JSON is also exposed at `/api/photos`.
- **Resilient**: missing images show a banner and placeholder tiles instead of a broken page.
- **Production server**: gunicorn, non-root user, health check, long cache headers on images.
- Ideas: view counter or "favorite" button stored in the course container's Redis, captions in MySQL, upload form.
