def get_color_name(h, s, v):
    """Detect the closest color name based on HSV values."""
    if h < 10 and s > 100:
        return "Red"
    elif 20 < h < 30 and s > 100:
        return "Yellow"
    elif 35 < h < 85 and s > 100:
        return "Green"
    elif 100 < h < 130 and s > 100:
        return "Blue"
    elif 130 < h < 170 and s > 100:
        return "Purple"
    return "Unknown"
