from typing import List, Literal

from pydantic import BaseModel
from nonebot.adapters.cqhttp import Message, MessageSegment
from nonebot.adapters.cqhttp.event import Sender

a = Message(
    **{
        "data": {
            "text": "CPU使用率: 5.00%\n内存使用率: bot: 8.78% | used: 32.70%\nbot: 345.60 MB | used: 1234.27 MB | total: 3936.10 MB"
        },
        "type": "text",
    }
)


class MessageGot(BaseModel):
    message_id: int
    real_id: int
    sender: Sender
    time: int
    message: Message
    raw_message: str


class GroupMessageGot(MessageGot):
    group_id: int
    message_type: Literal["group"]


print(
    MessageGot(
        **{
            "group": True,
            "group_id": 521656488,
            "message": [
                {
                    "data": {
                        "text": "CPU使用率: 5.00%\n内存使用率: bot: 8.78% | used: 32.70%\nbot: 345.60 MB | used: 1234.27 MB | total: 3936.10 MB"
                    },
                    "type": "text",
                },
                {
                    "data": {
                        "file": "e0e82fb9bbf723cc699019eddd94b1e5.image",
                        "subType": "0",
                        "url": "https://gchat.qpic.cn/gchatpic_new/1/0-0-E0E82FB9BBF723CC699019EDDD94B1E5/0?term=2",
                    },
                    "type": "image",
                },
            ],
            "message_id": -1746015371,
            "message_seq": 2983,
            "message_type": "group",
            "raw_message": "CPU使用率: 5.00%\n内存使用率: bot: 8.78% | used: 32.70%\nbot: 345.60 MB | used: 1234.27 MB | total: 3936.10 MB[CQ:image,file=e0e82fb9bbf723cc699019eddd94b1e5.image,subType=0]",
            "real_id": 2983,
            "sender": {"nickname": "Takker", "user_id": 1609225832},
            "time": 1636638774,
        }
    )
)


class ForwardMsg(BaseModel):
    content: List[MessageSegment]
    sender: Sender
    time: int


b = ForwardMsg(
    **{
        "content": [
            {"data": {"text": "两仪滚 正在直播：\n【滚  病友之间\n"}, "type": "text"},
            {
                "data": {
                    "file": "e7270e0b5eb41b6dec400287cd00cb4c.image",
                    "url": "https://c2cpicdw.qpic.cn/offpic_new/0//2330705135-2353581008-E7270E0B5EB41B6DEC400287CD00CB4C/0?term=2",
                },
                "type": "image",
            },
            {"data": {"text": "\n"}, "type": "text"},
            {"data": {"text": "https://live.bilibili.com/388"}, "type": "text"},
        ],
        "sender": {"nickname": "风屿测试bot", "user_id": 3147315517},
        "time": 1636712312,
        "extra": 1243,
    }
)

print(b)
