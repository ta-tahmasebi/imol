import os

from PIL import Image

from .svg_handler import svg_to_image


def open_image(path: str) -> Image.Image:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    if ext == "svg":
        return svg_to_image(path)

    return Image.open(path)


def save_image(img: Image.Image, path: str, format_name: str, **save_kwargs) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    img.save(path, format=format_name, **save_kwargs)


def make_output_path(input_path: str, output_ext: str) -> str:
    base, _ = os.path.splitext(input_path)
    return f"{base}.{output_ext.lstrip('.')}"
