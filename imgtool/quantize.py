from typing import Optional

import numpy as np
from PIL import Image

try:
    from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN
except ImportError:
    KMeans = None
    MiniBatchKMeans = None
    DBSCAN = None


def _require(lib, name: str):
    if lib is None:
        raise RuntimeError(f"{name} requires scikit-learn to be installed")


def quantize_median(img: Image.Image, k: int) -> Image.Image:
    return img.convert("RGB").quantize(colors=k, method=Image.Quantize.MEDIANCUT).convert("RGB")


def quantize_uniform(img: Image.Image, k: int) -> Image.Image:
    return img.convert("RGB").quantize(colors=k, method=Image.Quantize.FASTOCTREE).convert("RGB")


def quantize_kmeans(img: Image.Image, k: int) -> Image.Image:
    _require(KMeans, "kmeans")

    arr = np.asarray(img.convert("RGB"))
    h, w, _ = arr.shape
    pixels = arr.reshape(-1, 3)

    model = KMeans(n_clusters=k, n_init="auto")
    labels = model.fit_predict(pixels)
    centers = model.cluster_centers_.astype("uint8")

    out = centers[labels].reshape(h, w, 3)
    return Image.fromarray(out, "RGB")


def quantize_minibatch(img: Image.Image, k: int) -> Image.Image:
    _require(MiniBatchKMeans, "minibatch")

    arr = np.asarray(img.convert("RGB"))
    h, w, _ = arr.shape
    pixels = arr.reshape(-1, 3)

    model = MiniBatchKMeans(n_clusters=k, batch_size=4096)
    labels = model.fit_predict(pixels)
    centers = model.cluster_centers_.astype("uint8")

    out = centers[labels].reshape(h, w, 3)
    return Image.fromarray(out, "RGB")


def quantize_dbscan(
        img: Image.Image,
        eps: float,
        min_samples: int,
        max_colors: Optional[int],
) -> Image.Image:
    _require(DBSCAN, "dbscan")

    arr = np.asarray(img.convert("RGB"))
    h, w, _ = arr.shape
    pixels = arr.reshape(-1, 3).astype("float32")

    model = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
    labels = model.fit_predict(pixels)

    valid = labels >= 0
    if not valid.any():
        raise RuntimeError("DBSCAN found no clusters")

    uniq = np.unique(labels[valid])

    centers = []
    counts = []

    for u in uniq:
        cluster = pixels[labels == u]
        centers.append(cluster.mean(axis=0))
        counts.append(len(cluster))

    centers = np.array(centers)
    counts = np.array(counts)

    if max_colors and len(centers) > max_colors:
        idx = np.argsort(counts)[-max_colors:]
        centers = centers[idx]
        label_map = {uniq[i]: j for j, i in enumerate(idx)}
    else:
        label_map = {u: i for i, u in enumerate(uniq)}

    out = np.zeros_like(arr, dtype="uint8")
    flat = out.reshape(-1, 3)

    for i, px in enumerate(pixels):
        lbl = labels[i]
        if lbl == -1 or lbl not in label_map:
            d = np.linalg.norm(centers - px, axis=1)
            flat[i] = centers[d.argmin()]
        else:
            flat[i] = centers[label_map[lbl]]

    return Image.fromarray(out, "RGB")
