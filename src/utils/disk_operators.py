import os

from globals import UPLOADS_PATH


def get_images():
    return os.listdir(UPLOADS_PATH)

def write_image(image_file, filename, extension):
    full_image_name = str(filename) + extension
    image_file.save(os.path.join(UPLOADS_PATH, full_image_name))