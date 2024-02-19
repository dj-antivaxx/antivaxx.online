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
        # pil_image = Image.open(image)
        parsed_images.append({
            'file': image,
            'filename': image_filename,
            'resolution': 'None', #str(pil_image.size),
            'size': 'None', #str(image.tell()),
            'extension': os.path.splitext(image_filename)[1]
        })
    return parsed_images
