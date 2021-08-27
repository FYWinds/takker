import numpy
from PIL import Image
from typing import Dict
from matplotlib import pyplot
import multidict
from wordcloud import WordCloud, ImageColorGenerator


from configs.path_config import IMAGE_PATH, FONT_PATH


async def draw_word_cloud(gid: int, words: list):
    dic = multidict.MultiDict()
    ndic: Dict[str, int] = {}
    for w in words:
        for k in w.split(" "):
            val = ndic.get(k, 0)
            ndic.update({k: val + 1})
    for key in ndic:
        dic.add(key, ndic[key])
    mask = numpy.array(Image.open(f"{IMAGE_PATH}wordcloud/back.jpg"))
    wc = WordCloud(
        font_path=f"{FONT_PATH}/STKAITI.TTF",
        background_color="white",
        max_font_size=100,
        width=1920,
        height=1080,
        mask=mask,
    )
    wc.generate_from_frequencies(dic)
    image_colors = ImageColorGenerator(mask, default_color=(255, 255, 255))
    wc.recolor(color_func=image_colors)
    pyplot.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    pyplot.axis("off")
    wc.to_file(f"{IMAGE_PATH}wordcloud/temp/temp-{gid}.png")
    return f"{IMAGE_PATH}wordcloud/temp/temp-{gid}.png"
