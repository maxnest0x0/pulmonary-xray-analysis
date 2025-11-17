from typing import cast

import cv2
import numpy as np
from PIL import Image

from image import GrayscaleImage
from schemas import HeatmapPoint

type Heatmap[W: int, H: int] = np.ndarray[tuple[H, W], np.dtype[np.float32]]

def render_heatmap[W: int, H: int](
    image: GrayscaleImage[W, H],
    heatmap: Heatmap[W, H],
    alpha: float = 0.5,
    colormap: int = cv2.COLORMAP_JET,
) -> Image.Image:
    image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    heatmap_u8 = (heatmap * 255).astype(np.uint8)
    heatmap_bgr = cv2.applyColorMap(heatmap_u8, colormap)

    output_bgr = cv2.addWeighted(heatmap_bgr, alpha, image_bgr, 1 - alpha, 0)
    output = cv2.cvtColor(output_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(output)

def make_example_heatmap[W: int, H: int](
    width: W,
    height: H,
    center_x: float,
    center_y: float,
    sigma: float,
) -> Heatmap[W, H]:
    y, x = np.ogrid[:height, :width]
    output = np.exp(-((x - center_x) ** 2 + (y - center_y) ** 2) / (2 * sigma ** 2))
    return cast(Heatmap[W, H], output.astype(np.float32))

def dense_to_sparse(heatmap: Heatmap[int, int]) -> list[HeatmapPoint]:
    rows, cols = np.nonzero(heatmap)
    intensities = heatmap[rows, cols]
    return [
        HeatmapPoint(x.item(), y.item(), intensity.item())
        for x, y, intensity in zip(cols, rows, intensities)
    ]

def apply_threshold[W: int, H: int](
    heatmap: Heatmap[W, H],
    threshold: float = 0.1,
) -> Heatmap[W, H]:
    output = heatmap * (heatmap >= threshold)
    return cast(Heatmap[W, H], output)
