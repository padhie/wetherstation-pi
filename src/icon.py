def get_icon(kind):
    kind = kind.lower()

    if kind == "living":
        return [
            "########",
            "#......#",
            "#......#",
            "#......#",
            "#......#",
            "########",
            "...##...",
            "########",
        ]

    if kind == "sleep":
        return [
            "########",
            "#......#",
            "#..##..#",
            "#..##..#",
            "########",
            "#......#",
            "#......#",
            "########",
        ]

    if kind == "bath":
        return [
            "....#....",
            "...##....",
            "...#.#...",
            "..#...#..",
            ".#.....#.",
            ".#.....#.",
            "..#...#..",
            "...###...",
        ]

    if kind == "clear":
        return [
            ".........",
            "..#.##...",
            ".#.#..##.",
            "#.......#",
            "#.......#",
            ".#######.",
            ".........",
            ".........",
        ]

    return None

def draw_icon(draw, kind, x, y, scale=6):
    pixels = get_icon(kind)
    if pixels is None:
        print(f"unknown icon kind: {kind}")
        return

    for py, row in enumerate(pixels):
        for px, ch in enumerate(row):
            if ch == "#":
                draw.rectangle(
                    (x + px * scale, y + py * scale, x + (px + 1) * scale - 1, y + (py + 1) * scale - 1),
                    fill=0,
                )