from PIL import Image, ImageFilter
from io import BytesIO


def convert_image(raw):
    image = Image.open(BytesIO(raw)).convert('RGB')
    (w, h) = (1024, round(image.height * (1024/image.width)))
    image = image.resize((w, h))
    return image


def filter_image(image):
    image = image.filter(ImageFilter.SMOOTH_MORE)
    return image


def image_process(raw):
    return filter_image(convert_image(raw))
