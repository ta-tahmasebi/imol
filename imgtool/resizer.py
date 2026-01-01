from typing import Tuple

from PIL import Image


def resize_stretch(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    return img.resize(size, Image.Resampling.LANCZOS)


def resize_fit(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    img_copy = img.copy()
    img_copy.thumbnail(size, Image.Resampling.LANCZOS)
    return img_copy


def resize_fill(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    src_w, src_h = img.size

    scale = max(target_w / src_w, target_h / src_h)
    new_w = int(src_w * scale + 0.5)
    new_h = int(src_h * scale + 0.5)

    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    right = left + target_w
    bottom = top + target_h

    return resized.crop((left, top, right, bottom))
