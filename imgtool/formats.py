from typing import Dict

SUPPORTED_FORMATS: Dict[str, str] = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "bmp": "BMP",
    "tiff": "TIFF",
    "tif": "TIFF",
    "webp": "WEBP",
    "gif": "GIF",
    "ico": "ICO",
    "ppm": "PPM",
    "pgm": "PPM",
    "pbm": "PPM",
    "tga": "TGA",
    "pcx": "PCX",
    "xbm": "XBM",
    "xpm": "XPM",
    "psd": "PSD",
    "eps": "EPS",
    "avif": "AVIF",
}


def is_supported(ext: str) -> bool:
    return ext.lower().lstrip(".") in SUPPORTED_FORMATS


def to_pillow(ext: str) -> str:
    return SUPPORTED_FORMATS[ext.lower().lstrip(".")]
