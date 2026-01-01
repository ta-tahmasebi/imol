from typing import Optional
from .formats import is_supported, to_pillow
from .io import open_image, save_image, make_output_path


def convert_to_format(input_path: str, output_ext: str, output_path: Optional[str] = None) -> str:
    if not is_supported(output_ext):
        raise ValueError(f"Unsupported target type: {output_ext}")

    fmt = to_pillow(output_ext)
    if output_path is None:
        output_path = make_output_path(input_path, output_ext)

    with open_image(input_path) as img:
        if getattr(img, "is_animated", False):
            img.seek(0)
        if fmt == "JPEG" and img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        save_image(img, output_path, fmt)

    return output_path