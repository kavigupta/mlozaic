import numpy as np

COLORS = {
    "black": [0, 0, 0],
    "white": [255, 255, 255],
    "red": [255, 0, 0],
    "orange": [255, 128, 0],
    "yellow": [255, 255, 0],
    "green": [0, 255, 0],
    "cyan": [0, 255, 255],
    "blue": [0, 0, 255],
    "darkblue": [0, 0, 128],
    "pink": [255, 128, 128],
}

COLOR_TO_IDX = {name: idx for idx, name in enumerate(sorted(COLORS))}

IDX_TO_RGB = np.array([v for _, v in sorted(COLORS.items())], dtype=np.uint8)
