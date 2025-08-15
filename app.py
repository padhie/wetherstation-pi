#!/usr/bin/env python3
from PIL import Image, ImageFont

from src.setting import generate as generate_setting
from src.dashboard import render as render_dashboard

# ====== MAIN ======
if __name__ == "__main__":
    try:
        settings = generate_setting()
        img = render_dashboard(settings)

        if settings.eink.active:
            print("show on display")
            from src.eink import eink
        else:
            image_file = f"out/{settings.eink.debugImg}"
            img.save(image_file)
            print(f"save Image: {image_file}")

    except Exception as e:
        print("Error:", e)
