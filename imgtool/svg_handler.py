import io

try:
    import cairosvg
except ImportError:
    cairosvg = None

from PIL import Image


def svg_to_image(path: str) -> Image.Image:
    if cairosvg is None:
        raise RuntimeError("SVG support requires cairosvg")

    png_bytes = cairosvg.svg2png(url=path)
    return Image.open(io.BytesIO(png_bytes))
