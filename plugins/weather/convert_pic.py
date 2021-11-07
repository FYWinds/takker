from PIL import Image, ImageDraw, ImageFont

from configs.path_config import FONT_PATH, IMAGE_PATH

font = f"{FONT_PATH}/weather.ttc"
icon_dir = f"{IMAGE_PATH}/weather/icon/"
backgroud_dir = f"{IMAGE_PATH}/weather/backgroud.png"


def size(size: int):
    return ImageFont.truetype(font, size)


def load_icon(id: str, size: float = 1.0):
    im = Image.open(icon_dir + id + ".png")
    resize = (int(im.width * size), int(im.height * size))
    icon = im.thumbnail(resize, Image.ANTIALIAS)
    icon = im.convert("RGBA")
    return icon


def load_background(dir: str):
    im = Image.open(dir)


def draw(data: dict):
    # load backgroud picture
    im = Image.new("RGB", (1000, 1600), "white")
    d = ImageDraw.Draw(im)
    bg = Image.open(backgroud_dir)
    im.paste(bg, (0, 0), bg)

    # city
    city = ""
    for i in data["city"]:
        city += i + f"\n"
    d.multiline_text(
        (94, 113), city, fill="white", font=size(144), align="center", spacing=30
    )

    # now
    icon = load_icon(data["now"]["icon"])
    im.paste(icon, (600, 100), icon)
    d.text(
        (721, 362),
        data["now"]["text"],
        fill="white",
        font=size(80),
        align="center",
        anchor="mt",
    )
    d.text(
        (721, 455),
        data["now"]["temp"] + "°C",
        fill="white",
        font=size(100),
        align="center",
        anchor="mt",
    )
    d.text((721, 600), "(实时)", fill="white", font=size(50), align="center", anchor="mt")

    # mid box
    icon = load_icon(data["day1"]["iconDay"], size=0.5)
    im.paste(icon, (320, 870), icon)
    icon = load_icon(data["day1"]["iconNight"], size=0.5)
    im.paste(icon, (420, 970), icon)

    text = f"紫外线指数：" + f"\n相对湿度：" + f"\n降水量：" + f"\n能见度："
    d.multiline_text(
        (567, 890), text, fill="black", font=size(30), align="left", spacing=10
    )
    text = (
        f"{data['day1']['uvIndex']}"
        + f"\n{data['day1']['humidity']} %"
        + f"\n{data['day1']['precip']} mm"
        + f"\n{data['day1']['vis']} km"
    )
    d.multiline_text(
        (770, 890), text, fill="black", font=size(30), align="right", spacing=10
    )

    # button box
    icon = load_icon(data["day2"]["iconDay"], size=0.5)
    im.paste(icon, (105, 1253), icon)
    icon = load_icon(data["day2"]["iconNight"], size=0.5)
    im.paste(icon, (199, 1344), icon)

    d.text(
        (430, 1269),
        data["day2"]["tempMax"],
        fill="black",
        font=size(60),
        anchor="rt",
        align="left",
    )
    d.text((490, 1269), "°C", fill="black", font=size(60), anchor="mt")

    d.text(
        (430, 1424),
        data["day2"]["tempMin"],
        fill="black",
        font=size(60),
        anchor="rs",
        align="left",
    )
    d.text((490, 1424), "°C", fill="black", font=size(60), anchor="ms")

    text = f"紫外线指数：" + f"\n相对湿度：" + f"\n降水量：" + f"\n能见度："
    d.multiline_text(
        (567, 1262), text, fill="black", font=size(30), align="left", spacing=10
    )
    text = (
        f"{data['day2']['uvIndex']}"
        + f"\n{data['day2']['humidity']} %"
        + f"\n{data['day2']['precip']} mm"
        + f"\n{data['day2']['vis']} km"
    )
    d.multiline_text(
        (770, 1262), text, fill="black", font=size(30), align="right", spacing=10
    )

    obsTime = data["now"]["obsTime"][5:10] + " " + data["now"]["obsTime"][11:16]
    d.text(
        (500, 1533), obsTime, fill="white", font=size(35), align="center", anchor="mt"
    )

    return im
