#!/usr/bin/env python3
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# ====== Environment ======
load_dotenv(dotenv_path=".env")
if os.path.exists(".env.local"):
    load_dotenv(dotenv_path=".env.local", override=True)
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
#FONT_PATH = "/usr/share/fonts/truetype/comic.ttf"  # Comic Sans / freie Version
FONT_PATH = os.getenv("FONT_PATH")
OW_APIKEY = os.getenv("OW_APIKEY")
OW_CITY = os.getenv("OW_CITY")

# ====== SETTINGS ======
USE_EINK = False
ENTITIES = {
    "living": ("sensor.sonoff_snzb_02d_temperatur", "sensor.sonoff_snzb_02d_luftfeuchtigkeit"),
    "sleep": ("sensor.sonoff_snzb_02d_temperatur", "sensor.sonoff_snzb_02d_luftfeuchtigkeit"),
    "bath": ("sensor.sonoff_snzb_02d_temperatur", "sensor.sonoff_snzb_02d_luftfeuchtigkeit"),
}
FONT_BIG = ImageFont.truetype(FONT_PATH, 50)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 40)

# ====== POSITIONS ======
DISPLAY_SIZE = (800, 480)
WIDTH = 800
HEIGHT = 480
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2
THIRD_HEIGHT = HEIGHT / 3
SIX_HEIGHT = HEIGHT / 6

# ====== FUNKTION: E-Ink ======
def display_on_eink(epd7in5_V2, img):
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.display(epd.getbuffer(img))
    epd.sleep()

# ====== FUNKTION: Home Assistant ======
def get_state(entity_id):
    url = f"{HA_URL}/api/states/{entity_id}"
    headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}
    r = requests.get(url, headers=headers, timeout=5)
    r.raise_for_status()
    return float(r.json()["state"])

# ====== FUNKTION: Weather ======
def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={OW_APIKEY}&q={OW_CITY}&aqi=no"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    data = r.json()

    temp_c = data["current"]["temp_c"]
    humidity = data["current"]["humidity"]
    condition = data["current"]["condition"]["text"]

    return temp_c, humidity, condition

# ====== FUNKTION: display ======
def draw_icon(draw, kind, x, y, scale=6):
    pixels = []
    kind = kind.lower()

    if kind == "living":
        pixels = [
            "########",
            "#......#",
            "#......#",
            "#......#",
            "#......#",
            "########",
            "...##...",
            "########",
        ]
    elif kind == "sleep":
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
    elif kind == "bath":
        pixels = [
            "....#....",
            "...##....",
            "...#.#...",
            "..#...#..",
            ".#.....#.",
            ".#.....#.",
            "..#...#..",
            "...###...",
        ]
    elif kind == "clear":
        pixels = [
            ".........",
            ".........",
            "..#.##...",
            ".#.#..##.",
            "#.......#",
            "#.......#",
            ".#######.",
            ".........",
        ]
    else:
        print(f"unknown icon kind: {kind}")

    # Zeichnen
    for py, row in enumerate(pixels):
        for px, ch in enumerate(row):
            if ch == "#":
                draw.rectangle(
                    (x + px * scale, y + py * scale, x + (px + 1) * scale - 1, y + (py + 1) * scale - 1),
                    fill=0,
                )

def render_lines(draw):
    # left-right separator
    draw.line((HALF_WIDTH, 20, HALF_WIDTH, HEIGHT - 20), fill=0, width=2)

    # left top-down separator
    draw.line((20, HALF_HEIGHT, HALF_WIDTH, HALF_HEIGHT), fill=0, width=2)

    # right seg1-seg2
    draw.line((HALF_WIDTH, THIRD_HEIGHT, WIDTH - 20, THIRD_HEIGHT), fill=0, width=2)

    # right seg2-seg3
    draw.line((HALF_WIDTH, THIRD_HEIGHT * 2, WIDTH - 20, THIRD_HEIGHT * 2), fill=0, width=2)

def render_date_time(draw):
    now = datetime.now()
    date_str = now.strftime("%-d. %b %Y")
    time_str = now.strftime("%H:%M:%S")

    draw.text((20, (THIRD_HEIGHT / 2) - 20), date_str, font=FONT_BIG, fill=0)
    draw.text((20, (THIRD_HEIGHT / 2) + 50), time_str, font=FONT_BIG, fill=0)

def render_weather(draw):
    temp, humidity, condition = get_weather(OW_CITY)

    draw_icon(draw, condition, 20, HALF_HEIGHT + 50, 8)
    draw.text((110, HALF_HEIGHT + 50), OW_CITY, font=FONT_BIG, fill=0)
    write_state(draw, FONT_BIG, 20, HALF_HEIGHT + 120, temp, humidity)

def write_state(draw, font, x, y, temp, humidity):
    text = f"{temp:.0f} °C / {humidity:.0f}%"
    draw.text((x, y), text, font=font, fill=0)

def render_small_segment(draw, data, identifier, y):
    draw_icon(draw, identifier, HALF_WIDTH + 20, y)
    write_state(draw, FONT_SMALL, HALF_WIDTH + 80, y, data[identifier][0], data[identifier][1])

def render_dashboard(data):
    img = Image.new("1", DISPLAY_SIZE, 255)
    draw = ImageDraw.Draw(img)

    render_lines(draw)

    # left side
    render_date_time(draw)
    render_weather(draw)

    # right side
    render_small_segment(draw, data, "living", THIRD_HEIGHT / 3)
    render_small_segment(draw, data, "sleep", THIRD_HEIGHT + (THIRD_HEIGHT / 3))
    render_small_segment(draw, data, "bath", (THIRD_HEIGHT * 2) + (THIRD_HEIGHT / 3))

    return img

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
            print("show on display")
            # from waveshare_epd import epd7in5_V2  # Beispiel für 7.5" Waveshare
            # display_on_eink(epd7in5_V2, img)
        else:
            img.save("out/dashboard_preview.png")
            print("Bild gespeichert: dashboard_preview.png")

    except Exception as e:
        print("Fehler:", e)
