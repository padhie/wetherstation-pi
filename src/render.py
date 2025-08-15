from datetime import datetime
from src.weather import get_weather
from src.icon import draw_icon

def render_lines(display, position, draw):
    
    # left-right separator
    draw.line((position.halfWidth, 20, position.halfWidth, display.height - 20), fill=0, width=2)

    # left top-down separator
    draw.line((20, position.halfHeight, position.halfWidth, position.halfHeight), fill=0, width=2)

    # right seg1-seg2
    draw.line((position.halfWidth, position.thirdHeight, display.width - 20, position.thirdHeight), fill=0, width=2)

    # right seg2-seg3
    draw.line((position.halfWidth, position.thirdHeight * 2, display.width - 20, position.thirdHeight * 2), fill=0, width=2)

def write_state(draw, font, x, y, temp, humidity):
    text = f"{temp:.0f} °C / {humidity:.0f}%"
    draw.text((x, y), text, font=font, fill=0)

def render_small_segment(draw, data, font, x_base, identifier, y):
    draw_icon(draw, identifier, x_base, y)
    write_state(draw, font, x_base + 60, y, data[identifier][0], data[identifier][1])

def render_weather(draw, open_weather, font, y_base):
    temp, humidity, condition = get_weather(open_weather)

    draw_icon(draw, condition, 20, y_base + 50, 8)
    draw.text((110, y_base + 50), open_weather.city, font=font, fill=0)
    write_state(draw, font, 20, y_base + 120, temp, humidity)

def render_date_time(draw, y, font):
    now = datetime.now()
    date_str = now.strftime("%-d. %b %Y")
    time_str = now.strftime("%H:%M:%S")

    draw.text((20, y - 20), date_str, font=font, fill=0)
    draw.text((20, y + 50), time_str, font=font, fill=0)
