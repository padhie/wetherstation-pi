from dataclasses import dataclass

@dataclass
class Position:
    width: int
    height: int
    halfWidth: int
    halfHeight: int
    thirdHeight: int

def generate(settings):
    return Position(
        width = settings.display.width,
        height = settings.display.height,
        halfWidth = settings.display.width / 2,
        halfHeight = settings.display.height / 2,
        thirdHeight = settings.display.height / 3,
    )