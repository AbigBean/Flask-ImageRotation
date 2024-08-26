from PIL import Image
import os


def rotation_func(file_path: str, rotation: int) -> None:
    with Image.open(file_path) as img:
        rotated_img = img.rotate(rotation)
        rotated_img.save(file_path)

        