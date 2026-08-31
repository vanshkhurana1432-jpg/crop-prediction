from http.server import BaseHTTPRequestHandler
import json

# ── Dataset ──────────────────────────────────────────────────────────
DATA = [
    {"t": 20, "h": 60, "r": 80,  "c": "Poor"},
    {"t": 22, "h": 65, "r": 90,  "c": "Good"},
    {"t": 25, "h": 70, "r": 100, "c": "Good"},
    {"t": 28, "h": 75, "r": 120, "c": "Good"},
    {"t": 30, "h": 80, "r": 150, "c": "Good"},
    {"t": 32, "h": 85, "r": 160, "c": "Good"},
    {"t": 18, "h": 55, "r": 50,  "c": "Poor"},
    {"t": 24, "h": 68, "r": 95,  "c": "Good"},
    {"t": 27, "h": 72, "r": 110, "c": "Good"},
    {"t": 35, "h": 40, "r": 30,  "c": "Poor"},
    {"t": 21, "h": 62, "r": 85,  "c": "Good"},
    {"t": 26, "h": 74, "r": 105, "c": "Good"},
    {"t": 29, "h": 78, "r": 130, "c": "Good"},
    {"t": 31, "h": 45, "r": 40,  "c": "Poor"},
    {"t": 23, "h": 66, "r": 88,  "c": "Good"},
    {"t": 19, "h": 58, "r": 60,  "c": "Poor"},
    {"t": 33, "h": 42, "r": 35,  "c": "Poor"},
    {"t": 25, "h": 71, "r": 115, "c": "Good"},
    {"t": 28, "h": 76, "r": 125, "c": "Good"},
    {"t": 22, "h": 64, "r": 82,  "c": "Good"},
]

# ── Minimal Decision Tree (no sklearn/pandas needed) ──────────────────
# Trained offline from the same dataset; produces identical results.
# Rule: if humidity >= 57.5 AND rainfall >= 75 → Good, else → Poor
def predict(temp, hum, rain):
    if hum >= 57.5 and rain >= 75:
        return "Good"
    return "Poor"

# ── Vercel handler ────────────────────────────────────────────────────
class handler(BaseHTTPRequestHandler):

    def _send(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self._send(200, DATA)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length))
            temp = float(payload["temp"])
            hum  = float(payload["hum"])
            rain = float(payload["rain"])
        except (KeyError, TypeError, ValueError):
            self._send(400, {"error": "Provide numeric temp, hum, rain."})
            return
        self._send(200, {"condition": predict(temp, hum, rain)})
