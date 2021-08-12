import string


def cut_text(str, cut):
    """
    :说明: `get_cut_str`
    > 长文本自动换行切分

    :参数:
      * `str: [type]`: 文本
      * `cut: [type]`: 换行宽度，至少大于20

    :返回:
      - `List`: 切分后的文本列表
    """
    punc = """，,、。.？?）》】“"‘'；;：:！!·`~%^& """
    si = 0
    i = 0
    next_str = str
    str_list = []
    for s in next_str:
        if s in string.printable:
            si += 1
        else:
            si += 2
        i += 1
        if next_str[0] == "\n":
            next_str = next_str[1:]
        elif s == "\n":
            str_list.append(next_str[: i - 1])
            next_str = next_str[i - 1 :]
            si = 0
            i = 0
            continue
        if si > cut:
            try:
                if next_str[i] in punc:
                    i += 1
                if next_str[i] in string.ascii_letters:
                    for j in range(i, i - 16, -1):
                        if next_str[j] == " ":
                            i = j + 1
                            break
            except IndexError:
                str_list.append(next_str)
                return str_list
            str_list.append(next_str[:i])
            next_str = next_str[i:]
            si = 0
            i = 0
    str_list.append(next_str)
    i = 0
    non_wrap_str = []
    for p in str_list:
        if p[-1] == "\n":
            p = p[:-1]
        non_wrap_str.append(p)
        i += 1
    return non_wrap_str


text = """Commission spokesman Mi Feng said on Monday that the number of existing imported cases nationwide had been declining consistently in the past week, but the risk of new infections entering through the country's land crossings is increasing, giving rise to locally transmitted clusters of infection.
"We need to resolutely guard our borders and key border cities, improving their testing and treatment capacities, overcoming shortcomings and strengthening personal protections to cut off the spread of the virus," he said at a news conference.”
A wiki (/ˈwɪki/ (About this soundlisten) WIK-ee) is a hypertext publication collaboratively edited and managed by its own audience directly using a web browser. A typical wiki contains multiple pages for the subjects or scope of the project and could be either open to the public or limited to use within an organization for maintaining its internal knowledge base.
Wikis are enabled by wiki software, otherwise known as wiki engines. A wiki engine, being a form of a content management system, differs from other web-based systems such as blog software, in that the content is created without any defined owner or leader, and wikis have little inherent structure, allowing structure to emerge according to the needs of the users.[1] Wiki engines usually allow content to be written using a simplified markup language and sometimes edited with the help of a rich-text editor.[2] There are dozens of different wiki engines in use, both standalone and part of other software, such as bug tracking systems. Some wiki engines are open source, whereas others are proprietary. Some permit control over different functions (levels of access); for example, editing rights may permit changing, adding, or removing material. Others may permit access without enforcing access control. Other rules may be imposed to organize content.
但单纯的健康快乐也必定将会伴随着挫折。诚如歌德所言“未曾哭过长夜的人不足以语人生”，当我们在拒绝过度内卷的同时，但我们仍应去追求合理的卓越，去开创自己的人生，去丰富和开拓自己的视野，而不是只顾眼前之玩物，两耳不闻窗外事。
"""
result = cut_text(text, 23)
with open("text.txt", "w", encoding="utf-8") as f:
    f.write(str(result))
