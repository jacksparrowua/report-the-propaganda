import re
from enum import Enum

from telethon.tl.custom import Message


class ButtonAction(Enum):
    NEXT_TASK = 1
    SKIP_TASK = 2
    SKIP_BLOCKED_USER = 3


class ReportMessage:
    __is_telegram = "t.me/"
    __is_joinchat = "joinchat/"
    __message = None
    __message_body = None
    __message_items = None
    __message_buttons = None

    def __init__(self, message: Message):
        self.__message = message
        self.__message_body = message.message
        self.__message_items = self.__message_body.split("\n")

    def is_telegram(self) -> bool:
        return True if self.__is_telegram in self.__message_body else False

    def is_joinchat(self) -> bool:
        return True if self.__is_joinchat in self.__message_body else False

    def get_report_reason(self) -> str:
        return self.__message_items[3]

    def get_channel_name(self) -> str:
        if "joinchat/" in self.__message_items[6]:
            return self.__message_items[6].split("joinchat/")[-1]
        name = self.__message_items[6].split("t.me/")[-1]
        if "/" in name:
            name = name.split("/")[0]
        return name

    async def click_button(self, action: ButtonAction):
        buttons = await self.__message.get_buttons()
        await buttons[action.value][0].click()
