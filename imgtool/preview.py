import matplotlib.pyplot as plt
from PIL import Image


def show_side_by_side(original: Image.Image, result: Image.Image) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(original)
    axes[0].set_title("Original")
    axes[0].axis("off")

    axes[1].imshow(result)
    axes[1].set_title("Result")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()
