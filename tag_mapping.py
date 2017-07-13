TAG_MAP = {
    ('landuse', 'forest'): {"TYPE": "forest", "DRAW_TYPE": "plane"},
    ('natural', 'wood'): {"TYPE": "forest", "SUBTYPE": "natural", "DRAW_TYPE": "plane"}
}


def find_type(tags):
    keys = list(tags.items())

    return [TAG_MAP[key] for key in keys if key in TAG_MAP]
