from dataclasses import dataclass
from PIL import Image, ImageFont

@dataclass
class Font:
    path: str
    big: str
    small: str

def generate(settings):
    return Font(
        path = settings.fontPath,
        big = ImageFont.truetype(settings.fontPath, 50),
        small = ImageFont.truetype(settings.fontPath, 40),
    )