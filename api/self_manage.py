from ._api import BaseAPI


class SelfManagementAPI(BaseAPI):
    async def set_friend_add_request(
        self, flag: str, approve: bool, remark: str
    ) -> None:
        """
        :说明: `set_friend_add_request`
        > [**处理加好友请求**](https://docs.go-cqhttp.org/api/#%E5%A4%84%E7%90%86%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82)

        :参数:
          * `flag: str`: 加好友请求的 flag（需从上报的数据中获得）
          * `approve: bool`: 是否同意该好友请求
          * `remark: str`: 加好友后的好友备注（仅在同意时有效）
        """
        await self.call(
            "set_friend_add_request", flag=flag, approve=approve, remark=remark
        )

    async def delete_friend(self, friend_id: int) -> None:
        """
        :说明: `delete_friend`
        > [**删除好友**](https://docs.go-cqhttp.org/api/#%E5%88%A0%E9%99%A4%E5%A5%BD%E5%8F%8B)

        :参数:
          * `friend_id: int`: 好友 QQ 号
        """
        await self.call("delete_friend", friend_id=friend_id)
