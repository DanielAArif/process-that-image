from PIL import Image
from rembg import remove, new_session


session = new_session("u2netp")


def remove_background(image: Image.Image) -> Image.Image:
    result = remove(image, session=session)
    return result