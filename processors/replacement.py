from PIL import Image, ImageOps


def create_solid_background(
    size: tuple[int, int],
    color: str,
) -> Image.Image:
    """
    Membuat background warna solid dengan ukuran yang sama
    dengan gambar foreground.
    """
    return Image.new("RGBA", size, color)


def resize_background(
    background: Image.Image,
    target_size: tuple[int, int],
) -> Image.Image:
    """
    Menyesuaikan ukuran background dengan ukuran gambar utama
    menggunakan crop agar seluruh area terisi.
    """
    background = background.convert("RGBA")

    return ImageOps.fit(
        background,
        target_size,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )


def replace_background(
    foreground: Image.Image,
    background: Image.Image,
) -> Image.Image:
    """
    Menggabungkan foreground dengan background berdasarkan
    alpha channel hasil background removal.
    """
    foreground = foreground.convert("RGBA")
    background = resize_background(
        background,
        foreground.size,
    )

    return Image.alpha_composite(
        background,
        foreground,
    )