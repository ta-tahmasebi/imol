import argparse
from typing import Optional, Tuple

from imgtool.cropper import crop_image
from imgtool.formats import is_supported, to_pillow
from imgtool.io import open_image, make_output_path, save_image
from imgtool.preview import show_side_by_side
from imgtool.quantize import quantize_kmeans, quantize_dbscan, quantize_minibatch, quantize_uniform, quantize_median
from imgtool.resizer import resize_fit, resize_fill, resize_stretch


def parse_size(value: str) -> Tuple[int, int]:
    try:
        w, h = value.lower().split("x")
        return int(w), int(h)
    except Exception:
        raise argparse.ArgumentTypeError("Size must be WIDTHxHEIGHT (e.g. 800x600)")


def parse_box(value: str) -> Tuple[int, int, int, int]:
    try:
        parts = [int(x) for x in value.split(",")]
        if len(parts) != 4:
            raise ValueError
        return parts[0], parts[1], parts[2], parts[3]
    except Exception:
        raise argparse.ArgumentTypeError(
            "Crop must be LEFT,TOP,RIGHT,BOTTOM (e.g. 10,10,200,200)")


def parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="imol",
        description="a modular image tool", )

    parser.add_argument("input", help="Input image path")

    parser.add_argument(
        "-c", "--crop",
        type=parse_box,
        help="Crop box: LEFT,TOP,RIGHT,BOTTOM",
    )

    parser.add_argument(
        "-r", "--resize",
        type=parse_size,
        metavar="WxH",
        help="Resize image to WIDTHxHEIGHT",
    )

    parser.add_argument(
        "-m", "--resize-mode",
        choices=("fit", "fill", "stretch"),
        default="stretch",
        help="Resize mode (default: fit)",
    )

    parser.add_argument(
        "-t", "--to",
        help="Convert to target format (png, jpg, webp, avif, ...)",
    )

    parser.add_argument(
        "-o", "--output",
        help="Output path (optional)",
    )

    parser.add_argument(
        "-sh", "--show",
        action="store_true",
        help="Show original and processed images side by side after saving"
    )

    parser.add_argument(
        "-s", "--save",
        action="store_true",
        help="Save the output image",
    )

    parser.add_argument(
        "-z", "--size",
        action="store_true",
        help="Print main image size (width x height)",
    )

    parser.add_argument(
        "-cm", "--cluster-method",
        choices=("median", "kmeans", "minibatch", "octree", "uniform", "dbscan"),
        default="median",
        help="Color clustering method (default: median)",
    )

    parser.add_argument(
        "-k", "--colors",
        type=int,
        help="Target number of colors (ignored by dbscan)",
    )

    parser.add_argument(
        "-db", "--dbscan",
        action="store_true",
        help="Use DBSCAN clustering (overrides --cluster-method)",
    )

    parser.add_argument(
        "-de", "--dbscan-eps",
        type=float,
        default=8.0,
        help="DBSCAN epsilon (color distance threshold)",
    )

    parser.add_argument(
        "-dm", "--dbscan-min-samples",
        type=int,
        default=100,
        help="DBSCAN minimum samples per cluster",
    )

    parser.add_argument(
        "-mc", "--max-colors",
        type=int,
        help="Maximum number of colors for DBSCAN output",
    )

    return parser.parse_args(argv)


def run_cli(argv: Optional[list] = None) -> int:
    args = parse_args(argv)

    try:
        with open_image(args.input) as img:
            original = img.copy()

            if args.size:
                print(f"Image size: {img.width}x{img.height}")
                print("Exiting...")
                return 0

            if args.crop:
                img = crop_image(img, args.crop)

            if args.resize:
                if args.resize_mode == "fit":
                    img = resize_fit(img, args.resize)
                elif args.resize_mode == "fill":
                    img = resize_fill(img, args.resize)
                else:
                    img = resize_stretch(img, args.resize)

            if args.to:
                if not is_supported(args.to):
                    raise ValueError(f"Unsupported target format: {args.to}")
                fmt = to_pillow(args.to)
                out_path = args.output or make_output_path(args.input, args.to)
            else:
                fmt = None
                out_path = args.output or make_output_path(args.input, "png")

            if args.save:
                save_image(img, out_path, format_name=fmt)
                print(out_path)

            if args.dbscan or args.cluster_method == "dbscan":
                img = quantize_dbscan(
                    img,
                    eps=args.dbscan_eps,
                    min_samples=args.dbscan_min_samples,
                    max_colors=args.max_colors,
                )

            elif args.colors:
                if args.cluster_method == "kmeans":
                    img = quantize_kmeans(img, args.colors)
                elif args.cluster_method == "minibatch":
                    img = quantize_minibatch(img, args.colors)
                elif args.cluster_method == "uniform":
                    img = quantize_uniform(img, args.colors)
                else:
                    img = quantize_median(img, args.colors)

            if getattr(args, "show", False):
                show_side_by_side(original, img)

        return 0

    except Exception as exc:
        print(f"Error: {exc}")
        return 1


def main():
    raise SystemExit(run_cli())
