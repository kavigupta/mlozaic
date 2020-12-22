import numpy as np

from .colors import COLOR_TO_IDX, IDX_TO_RGB


def invert_transform(t, coordinates):
    assert t.shape == (3, 3)
    A = t[:2, :2]
    b = t[:2, 2]

    shifted = coordinates - b[:, None, None]
    shifted = shifted.reshape(2, -1)
    rescaled = np.linalg.inv(A) @ shifted
    rescaled = rescaled.reshape(*coordinates.shape)
    return rescaled


def forward_transform(t, coordinates):
    assert t.shape == (3, 3)
    A = t[:2, :2]
    b = t[:2, 2]

    scaled = (A @ coordinates.reshape(2, -1)).reshape(*coordinates.shape)
    shifted = coordinates + b[:, None, None]
    return shifted


def render(items, size=(100, 100), stretch=10, background="white", rgb=True):
    w, h = size
    x, y = np.meshgrid(
        np.arange(w * stretch) / stretch - w / 2,
        h / 2 - np.arange(h * stretch) / stretch,
    )
    coords = np.array([x, y])
    image = (
        np.zeros((w * stretch, h * stretch), dtype=np.uint8) + COLOR_TO_IDX[background]
    )
    for item in items:
        try:
            trans_coords = invert_transform(item.transform, coords)
        except np.linalg.LinAlgError:
            continue
        mask = item.type(*trans_coords)
        image[mask] = COLOR_TO_IDX[item.color]
    if not rgb:
        return image
    return IDX_TO_RGB[image]
