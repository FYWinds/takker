from typing import Union, Optional

from .info import InfoAPI
from .message import MessageAPI
from .self_manage import SelfManagementAPI
from .group_manage import GroupManagementAPI


class API(GroupManagementAPI, InfoAPI, MessageAPI, SelfManagementAPI):
    def __init__(self, bot_id: Optional[Union[int, str]] = None) -> None:
        super().__init__(bot_id)


api = API()
