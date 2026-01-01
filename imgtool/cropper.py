from typing import Tuple
from PIL import Image


def crop_image(img: Image.Image, box: Tuple[int, int, int, int]) -> Image.Image:
    return img.crop(box)