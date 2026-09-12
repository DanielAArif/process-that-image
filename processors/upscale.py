from pathlib import Path

import cv2
from PIL import Image


MODEL_DIR = Path(__file__).parent.parent / "models"


def upscale_image(
    image: Image.Image,
    scale: int,
) -> Image.Image:

    if scale not in (2, 4):
        raise ValueError("Scale must be 2 or 4.")

    model_path = MODEL_DIR / f"FSRCNN_x{scale}.pb"

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found: {model_path}"
        )

    # PIL -> OpenCV
    image_rgb = image.convert("RGB")

    image_cv = cv2.cvtColor(
        __import__("numpy").array(image_rgb),
        cv2.COLOR_RGB2BGR,
    )

    # Create super-resolution model
    sr = cv2.dnn_superres.DnnSuperResImpl_create()

    sr.readModel(str(model_path))

    sr.setModel(
        "fsrcnn",
        scale,
    )

    # Upscale
    result = sr.upsample(image_cv)

    # OpenCV -> PIL
    result_rgb = cv2.cvtColor(
        result,
        cv2.COLOR_BGR2RGB,
    )

    return Image.fromarray(result_rgb)