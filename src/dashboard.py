#!/usr/bin/env python3
from PIL import Image, ImageDraw

from src.home_assistant import get_state
from src.position import generate as generate_position
from src.font import generate as generate_font
from src.render import render_lines, render_small_segment, render_weather, render_date_time

# ====== SETTINGS ======
ENTITIES = {
    "living": ("sensor.sonoff_snzb_02d_temperatur", "sensor.sonoff_snzb_02d_luftfeuchtigkeit"),
    "sleep": ("sensor.sonoff_snzb_02d_temperatur", "sensor.sonoff_snzb_02d_luftfeuchtigkeit"),
    "bath": ("sensor.sonoff_snzb_02d_temperatur", "sensor.sonoff_snzb_02d_luftfeuchtigkeit"),
}


def render(settings):
    position = generate_position(settings)
    font = generate_font(settings)

    img = Image.new("1", (position.width, position.height), 255)
    draw = ImageDraw.Draw(img)

    render_lines(settings.display, position, draw)

    # left side
    render_date_time(draw, (position.thirdHeight / 2), font.big)
    render_weather(draw, settings.openWeather, font.big, position.halfHeight)

    # right side
    sensor_data = {}
    for key, (t_ent, h_ent) in ENTITIES.items():
        sensor_data[key] = (get_state(settings.homeAssistant, t_ent), get_state(settings.homeAssistant, h_ent))

    render_small_segment(draw, sensor_data, font.small, position.halfWidth + 20, "living", position.thirdHeight / 3)
    render_small_segment(draw, sensor_data, font.small, position.halfWidth + 20, "sleep", position.thirdHeight + (position.thirdHeight / 3))
    render_small_segment(draw, sensor_data, font.small, position.halfWidth + 20, "bath", (position.thirdHeight * 2) + (position.thirdHeight / 3))

    return img
