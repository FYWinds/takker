# Author djkcyl/ABot-Graia
# Edit by FYWinds
import string


def cut_text(str, cut):
    """
    :说明: `get_cut_str`
    > 长文本自动换行切分

    :参数:
      * `str: [type]`: 文本
      * `cut: [type]`: 换行宽度，请至少大于20

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


def align(str: str, num: int, type: str = "left") -> str:
    length = 0
    for c in str:
        if c in string.printable:
            length += 1
        else:
            length += 2
    diff = num - length
    if type == "left":
        return str + " " * diff
    elif type == "right":
        return " " * diff + str
    elif type == "center":
        return str.center(num)
    else:
        return str
