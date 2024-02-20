import os

from werkzeug.utils import secure_filename
from PIL import Image

def parse_content(content):
    return content.replace('\r\n', '<br>')

def parse_request_images(images_list):
    if not any(image.filename for image in images_list):
        return None
    parsed_images = []    
    for image in images_list:
        image_filename = secure_filename(image.filename)
    
        with Image.open(image) as pil_image:
            resolution_x, resolution_y = pil_image.size
            size = pil_image.tell()
        image.seek(0)

        parsed_images.append({
            'file': image,
            'filename': image_filename,
            'resolution_x': resolution_x,
            'resolution_y': resolution_y,
            'size': size,
            'extension': os.path.splitext(image_filename)[1]
        })
    return parsed_images
