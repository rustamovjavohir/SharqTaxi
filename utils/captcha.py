from io import BytesIO

from PIL import Image
from captcha.image import ImageCaptcha


def generate_captcha(text="Hello captcha", height=80, width=160) -> Image:
    """
    Generate captcha image and returns it with bytes data
    """
    captcha: ImageCaptcha = ImageCaptcha(width=width, height=height)
    data: BytesIO = captcha.generate(text)
    # captcha.write(text, 'captcha.png')
    image = Image.open(data)
    # image.show()
    return image
