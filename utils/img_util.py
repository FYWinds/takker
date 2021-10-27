import base64
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from utils.text_util import cut_text
from configs.path_config import FONT_PATH


def imageToB64(image: Image.Image) -> str:
    """
    :说明: `imageToB64`
    > PIL Image转base64

    :参数:
      * `image: Image.Image`: Image对象

    :返回:
      - `str`: base64://xxxxxxxx
    """
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    base64_str = base64.b64encode(buffer.getvalue()).decode()
    return "base64://" + base64_str


# 从Abot抄来的文字转图片
async def textToImage(text: str, cut=64) -> str:
    """
    :说明: `textToImage`
    > 文字转图片

    :参数:
      * `text: str`: 要转换的文字内容

    :可选参数:
      * `cut: int = 64`: 自动换行字符数限制

    :返回:
      - `str`: 图片Base64，base64://xxxxxxxx
    """
    font = ImageFont.truetype(f"{FONT_PATH}sarasa-mono-sc-semibold.ttf", 22)
    cut_str = "\n".join(cut_text(text, cut))
    textx, texty = font.getsize_multiline(cut_str)
    image = Image.new("RGB", (textx + 50, texty + 50), (242, 242, 242))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), cut_str, font=font, fill=(31, 31, 33))
    imageb64 = imageToB64(image)
    return imageb64
