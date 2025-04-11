from PIL import Image
import pillow_heif
import os

def open_image_safe(path: str, target_size: tuple[int, int] = (512, 512)) -> Image.Image:
    """
    Открывает изображение и приводит его к RGB + заданному размеру.
    Поддерживает HEIC, JPEG, PNG и т.д.

    :param path: путь до изображения
    :param target_size: кортеж (ширина, высота), до которого надо уменьшить изображение
    :return: Pillow Image
    """
    ext = os.path.splitext(path)[-1].lower()

    if ext in [".heic", ".heif"]:
        heif_file = pillow_heif.read_heif(path)
        image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
    else:
        image = Image.open(path)

    image = image.convert("RGB")
    image = image.resize(target_size, Image.LANCZOS)

    return image