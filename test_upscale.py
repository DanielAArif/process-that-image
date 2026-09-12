from PIL import Image

from processors.upscale import upscale_image


image = Image.open("test.jpg")

result = upscale_image(
    image,
    4,
)

result.save("test_upscaled.png")

print(
    f"Original : {image.size}"
)

print(
    f"Upscaled : {result.size}"
)