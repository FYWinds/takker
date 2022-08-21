import base64
from io import BytesIO
from typing import Tuple, Union, Literal, Optional
from pathlib import Path

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
async def textToImage(text: str, cut: int = 64) -> str:
    """
    :说明: `textToImage`
    > 文字转图片

    :参数:
      * `text: str`: 要转换的文字内容

    :可选参数:
      * `cut: int = 64`: 自动换行字符数限制, 设置为零禁用自动换行

    :返回:
      - `str`: 图片Base64，base64://xxxxxxxx
    """
    font = ImageFont.truetype(f"{FONT_PATH}sarasa-mono-sc-semibold.ttf", 22)
    if cut != 0:
        cut_str = "\n".join(cut_text(text, cut))
    else:
        cut_str = text
    textx, texty = font.getsize_multiline(cut_str)
    image = Image.new("RGB", (textx + 50, texty + 50), (242, 242, 242))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), cut_str, font=font, fill=(31, 31, 33))
    imageb64 = imageToB64(image)
    return imageb64


async def textToImageBuf(text: str, cut: int = 64) -> bytes:
    """
    :说明: `textToImageBuf`
    > 文字转图片，返回bytes

    :参数:
      * `text: str`: 要转换的文字内容, 设置为零禁用自动换行

    :可选参数:
      * `cut: int = 64`: 自动换行字符数限制

    :返回:
      - `bytes`: 图片bytes
    """
    font = ImageFont.truetype(f"{FONT_PATH}sarasa-mono-sc-semibold.ttf", 22)
    if cut != 0:
        cut_str = "\n".join(cut_text(text, cut))
    else:
        cut_str = text
    textx, texty = font.getsize_multiline(cut_str)
    image = Image.new("RGB", (textx + 50, texty + 50), (242, 242, 242))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), cut_str, font=font, fill=(31, 31, 33))
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


class ImageUtil:
    """
    :说明: `ImageUtil`
    > 图片处理工具类
    > Author: HibiKier
    """

    def __init__(
        self,
        width: int,
        height: int,
        paste_image_width: int = 0,
        paste_image_height: int = 0,
        color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]] = None,
        image_mode: Literal[
            "CMYK", "HSV", "LAB", "RGB", "RGBA", "RGBX", "YCbCr"
        ] = "RGBA",
        font_size: int = 10,
        background: Union[Optional[str], BytesIO, Path] = None,
        font: str = "sarasa-mono-sc-semibold.ttf",
        ratio: float = 1,
        is_alpha: bool = False,
        plain_text: Optional[str] = None,
        font_color: Optional[Tuple[int, int, int]] = None,
    ) -> None:
        """
        :说明: `__init__`
        > 创建图片处理对象

        :参数:
          * `width: int`: 图片宽度
          * `height: int`: 图片高度

        :可选参数:
          * `paste_image_width: int = 0`: 当图片做为背景图时，设置贴图的宽度，用于贴图自动换行
          * `paste_image_height: int = 0`: 当图片做为背景图时，设置贴图的高度，用于贴图自动换行
          * `color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]] = None`: 生成图片的颜色
          * `image_mode: Literal["CMYK", "HSV", "LAB", "RGB", "RGBA", "RGBX", "YCbCr"] = "RGBA"`: 图片类型
          * `font_size: int = 10`: 字体大小
          * `background: Union[Optional[str], BytesIO, Path] = None`: 背景图片路径
          * `font: str = "sarasa-mono-sc-semibold.ttf"`: 字体路径
          * `ratio: float = 1`: 图片缩放比例
          * `is_alpha: bool = False`: 是否使用透明度
          * `plain_text: Optional[str] = None`: 纯文本内容
          * `font_color: Optional[Tuple[int, int, int]] = None`: 字体颜色

        :错误:
          - `ValueError`: image_mode 不在范围内
        """
        self.width = width
        self.height = height
        self.paste_image_width = paste_image_width
        self.paste_image_height = paste_image_height
        self.current_width = 0
        self.current_height = 0
        self.font = ImageFont.truetype(f"{FONT_PATH}{font}", font_size)
        if image_mode not in ["CMYK", "HSV", "LAB", "RGB", "RGBA", "RGBX", "YCbCr"]:
            raise ValueError(f"image_mode: {image_mode}错误")
        if not color:
            color = (255, 255, 255)
        if not background:
            if plain_text:
                self.width = (
                    self.width
                    if self.width > self.font.getsize(plain_text)[0]
                    else self.font.getsize(plain_text)[1]
                )
                self.height = (
                    self.height
                    if self.height > self.font.getsize(plain_text)[1]
                    else self.font.getsize(plain_text)[1]
                )
            self.mark_image = Image.new(image_mode, (self.width, self.height), color)
            self.mark_image.convert(image_mode)
        else:
            if not width and not height:
                self.mark_image = Image.open(background)
                width, height = self.mark_image.size
                if ratio and ratio > 0 and ratio != 1:
                    self.width = int(ratio * width)
                    self.height = int(ratio * height)
                    self.mark_image = self.mark_image.resize(
                        (self.width, self.height), Image.ANTIALIAS
                    )
                else:
                    self.width = width
                    self.height = height
            else:
                self.mark_image = Image.open(background).resize(
                    (self.width, self.height), Image.ANTIALIAS
                )
        if is_alpha:
            array = self.mark_image.load()
            for i in range(width):
                for j in range(height):
                    pos = array[i, j]  # type: ignore
                    is_edit = sum([1 for x in pos[0:3] if x > 240]) == 3
                    if is_edit:
                        array[i, j] = (255, 255, 255, 0)  # type: ignore
        self.draw = ImageDraw.Draw(self.mark_image)
        self.size = self.width, self.height
        if plain_text:
            fill = font_color if font_color else (0, 0, 0)
            self.text((0, 0), plain_text, fill)

    def text(
        self,
        pos: Tuple[int, int],
        text: str,
        fill: Tuple[int, int, int] = (0, 0, 0),
        center_type: Literal["center", "by_height", "by_width"] = None,
    ):
        """
        :说明: `text`
        > 在图片上添加文本

        :参数:
          * `pos: Tuple[int, int]`: 文本位置
          * `text: str`: 文本内容

        :可选参数:
          * `fill: Tuple[int, int, int] = (0, 0, 0)`: 文本颜色
          * `center_type: Literal["center", "by_height", "by_width"] = None`: 文本居中方式

        :错误:
          * `ValueError`: 当 `center_type` 不为 `center`, `by_height`, `by_width` 时
        """
        if center_type:
            if center_type not in ["center", "by_height", "by_width"]:
                raise ValueError(
                    "center_type must be 'center', 'by_width' or 'by_height'"
                )
            width, height = self.width, self.height
            text_widht, text_height = self.getsize(text)
            if center_type == "center":
                width = int((width - text_widht) / 2)
                height = int((height - text_height) / 2)
            elif center_type == "by_width":
                width = int((width - text_widht) / 2)
                height = pos[1]
            elif center_type == "by_height":
                height = int((height - text_height) / 2)
                width = pos[0]
            pos = (width, height)
        self.draw.text(pos, text, fill=fill, font=self.font)

    def paste(
        self,
        img: Union["ImageUtil", Image.Image],
        pos: Tuple[int, int] = None,
        alpha: bool = False,
        center_type: Literal["center", "by_height", "by_width"] = None,
    ):
        """
        :说明: `paste`
        > 在图片上添加图片

        :参数:
          * `img: ImageUtil`: 图片对象

        :可选参数:
          * `pos: Tuple[int, int] = None`: 图片位置
          * `alpha: bool = False`: 是否使用透明度
          * `center_type: Literal["center", "by_height", "by_width"] = None`: 图片居中方式

        :错误:
          - `ValueError`: 当 `center_type` 不为 `center`, `by_height`, `by_width` 时
        """
        if center_type:
            if center_type not in ["center", "by_height", "by_width"]:
                raise ValueError(
                    "center_type must be 'center', 'by_width' or 'by_height'"
                )
            width, height = 0, 0
            if not pos:
                pos = (0, 0)
            if center_type == "center":
                width = int((self.width - img.width) / 2)
                height = int((self.height - img.height) / 2)
            elif center_type == "by_width":
                width = int((self.width - img.width) / 2)
                height = pos[1]
            elif center_type == "by_height":
                width = pos[0]
                height = int((self.height - img.height) / 2)
            pos = (width, height)
        if isinstance(img, ImageUtil):
            img = img.mark_image
        if self.current_width == self.width:
            self.current_width = 0
            self.current_height += self.paste_image_height
        if not pos:
            pos = (self.current_width, self.current_height)
        if alpha:
            try:
                self.mark_image.paste(img, pos, img)
            except ValueError:
                img = img.convert("RGBA")
                self.mark_image.paste(img, pos, img)
        else:
            self.mark_image.paste(img, pos)
        self.current_width += self.paste_image_width

    def getsize(self, msg: str) -> Tuple[int, int]:
        """
        :说明: `getsize`
        > 获取文本大小

        :参数:
          * `msg: str`: 文本内容

        :返回:
          - `Tuple[int, int]`: 文本大小
        """
        return self.font.getsize(msg)

    def point(self, pos: Tuple[int, int], fill: Tuple[int, int, int] = (0, 0, 0)):
        """
        :说明: `point`
        > 绘制单独的像素点

        :参数:
          * `pos: Tuple[int, int]`: 像素点位置

        :可选参数:
          * `fill: Tuple[int, int, int] = (0, 0, 0)`: 像素点颜色
        """
        self.draw.point(pos, fill=fill)

    def ellipse(
        self,
        pos: Tuple[int, int, int, int],
        fill: Optional[Tuple[int, int, int]] = None,
        outline: Optional[Tuple[int, int, int]] = None,
        width: int = 1,
    ):
        """
        :说明: `ellipse`
        > 绘制描边

        :参数:
          * `pos: Tuple[int, int, int, int]`: 坐标范围[x1, y1, x2, y2]

        :可选参数:
          * `fill: Optional[Tuple[int, int, int]] = None`: 填充颜色
          * `outline: Optional[Tuple[int, int, int]] = None`: 描边颜色
          * `width: int = 1`: 描边宽度
        """
        self.draw.ellipse(pos, fill, outline, width)

    def save(self, path: Union[str, Path]):
        """
        :说明: `save`
        > 保存图片

        :参数:
          * `path: Union[str, Path]`: 保存路径
        """
        if isinstance(path, Path):
            path = path.absolute()
        self.mark_image.save(path)

    def convert(
        self,
        image_mode: Literal[
            "CMYK", "HSV", "LAB", "RGB", "RGBA", "RGBX", "YCbCr"
        ] = "RGBA",
    ):
        """
        :说明: `convert`
        > 转换图片类型

        :可选参数:
          * `image_mode:Literal["CMYK", "HSV", "LAB", "RGB", "RGBA", "RGBX", "YCbCr"] = "RGBA"`: 转换后的图片类型
        """
        self.mark_image = self.mark_image.convert(image_mode)

    def circle(self):
        """
        :说明: `circle`
        > 转换图片为圆形
        """
        self.convert("RGBA")
        r2 = min(self.width, self.height)
        if self.width != self.height:
            self.resize(width=r2, height=r2)
        r3 = int(r2 / 2)
        imb = Image.new("RGBA", (r3 * 2, r3 * 2), (255, 255, 255, 0))
        pim_a = self.mark_image.load()  # 像素的访问对象
        pim_b = imb.load()
        r = float(r2 / 2)
        for i in range(r2):
            for j in range(r2):
                lx = abs(i - r)  # 到圆心距离的横坐标
                ly = abs(j - r)  # 到圆心距离的纵坐标
                length = (pow(lx, 2) + pow(ly, 2)) ** 0.5  # 三角函数 半径
                if length < r3:
                    pim_b[i - (r - r3), j - (r - r3)] = pim_a[i, j]  # type: ignore
        self.mark_image = imb

    def resize(self, ratio: float = 0, width: int = 0, height: int = 0):
        """
        :说明: `resize`
        > 图片缩放

        :可选参数:
          * `ratio: float = 0`: 缩放比例
          * `width: int = 0`: 缩放后的宽度
          * `height: int = 0`: 缩放后的高度

        :异常:
          - `Exception`: 缺少参数
        """
        if not width and not height and not ratio:
            raise Exception("缺少参数...")
        if not width and not height and ratio:
            width = int(self.width * ratio)
            height = int(self.height * ratio)
        self.mark_image = self.mark_image.resize((width, height), Image.ANTIALIAS)
        self.width, self.height = self.mark_image.size
        self.size = self.width, self.height
        self.draw = ImageDraw.Draw(self.mark_image)

    def toB64(self) -> str:
        """
        :说明: `toB64`
        > 返回Base64编码的图片

        :返回:
          - `str`: Base64编码的图片
        """
        buffer = BytesIO()
        self.mark_image.save(buffer, format="PNG")
        base64_str = base64.b64encode(buffer.getvalue()).decode()
        return base64_str
