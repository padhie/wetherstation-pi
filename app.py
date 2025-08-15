#!/usr/bin/env python3
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# ====== EINSTELLUNGEN ======
load_dotenv(dotenv_path=".env")
if os.path.exists(".env.local"):
    load_dotenv(dotenv_path=".env.local", override=True)
HA_URL = os.getenv("HA_URL")
TOKEN = os.getenv("HA_TOKEN")
USE_EINK = os.getenv("USE_EINK")

DISPLAY_SIZE = (800, 480)
FONT_PATH = "/usr/share/fonts/truetype/comic.ttf"  # Comic Sans / freie Version
ENTITIES = {
    "wohnzimmer": ("sensor.livingroom_temperature", "sensor.livingroom_humidity"),
    "schlafzimmer": ("sensor.bedroom_temperature", "sensor.bedroom_humidity"),
    "badezimmer": ("sensor.bathroom_temperature", "sensor.bathroom_humidity"),
}

# ====== FUNKTION: Daten aus Home Assistant ======
def get_state(entity_id):
    url = f"{HA_URL}/api/states/{entity_id}"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    r = requests.get(url, headers=headers, timeout=5)
    r.raise_for_status()
    return float(r.json()["state"])

# ====== FUNKTION: Pixel-Icons erstellen ======
def draw_icon(draw, kind, x, y, scale=2):
    # Icons in Pixel-Art (Größe: 8x8 Pixel) → hochskaliert
    pixels = []
    if kind == "sofa":  # Sofa (A)
        pixels = [
            "........",
            ".######.",
            "#......#",
            "#......#",
            "#......#",
            "########",
            "#......#",
            "########",
        ]
    elif kind == "bed":  # Bett (B)
        pixels = [
            "########",
            "#......#",
            "#..##..#",
            "#..##..#",
            "########",
            "#......#",
            "#......#",
            "########",
        ]
    elif kind == "shower":  # Dusche (C)
        pixels = [
            "..##....",
            ".#..#...",
            "#....#..",
            "######..",
            "...##...",
            "...##...",
            "..####..",
            "..####..",
        ]
    # Zeichnen
    for py, row in enumerate(pixels):
        for px, ch in enumerate(row):
            if ch == "#":
                draw.rectangle(
                    (x + px * scale, y + py * scale, x + (px + 1) * scale - 1, y + (py + 1) * scale - 1),
                    fill=0,
                )

# ====== FUNKTION: Dashboard rendern ======
def render_dashboard(data):
    img = Image.new("1", DISPLAY_SIZE, 255)  # 1-Bit Bild, Weiß
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype(FONT_PATH, 36)
    # font_small = ImageFont.truetype(FONT_PATH, 28)

    # Datum + Uhrzeit
    now = datetime.now()
    date_str = now.strftime("%-d. %b %Y")
    time_str = now.strftime("%H:%M")

    draw.text((20, 20), date_str, font=font_big, fill=0)
    draw.text((350, 20), time_str, font=font_big, fill=0)

    # Linienkoordinaten
    line_y = [70, 190, 310, 430]
    for y in line_y:
        draw.line((20, y, DISPLAY_SIZE[0] - 20, y), fill=0, width=2)

    # Bereiche A, B, C
    sections = {
        "wohnzimmer": {"pos": (20, 80), "icon": "sofa"},
        "schlafzimmer": {"pos": (20, 200), "icon": "bed"},
        "badezimmer": {"pos": (20, 320), "icon": "shower"},
    }

    for key, info in sections.items():
        x, y = info["pos"]
        temp, hum = data[key]
        draw_icon(draw, info["icon"], x, y, scale=4)
        text = f"({key}) {temp:.0f} °C / {hum:.0f}%"
        draw.text((x + 50, y + 10), text, font=font_big, fill=0)

    return img

# ====== FUNKTION: Dashboard rendern ======
def display_on_eink(epd7in5_V2, img):
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.display(epd.getbuffer(img))
    epd.sleep()

# ====== MAIN ======
if __name__ == "__main__":
    try:
        # Daten holen
        sensor_data = {}
        for key, (t_ent, h_ent) in ENTITIES.items():
            sensor_data[key] = (get_state(t_ent), get_state(h_ent))

        # Rendern
        img = render_dashboard(sensor_data)

        if USE_EINK:
            from waveshare_epd import epd7in5_V2  # Beispiel für 7.5" Waveshare
            display_on_eink(epd7in5_V2, img)
        else:
            img.save("dashboard_preview.png")
            print("Bild gespeichert: dashboard_preview.png")

    except Exception as e:
        print("Fehler:", e)
