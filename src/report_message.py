from enum import Enum

from telethon.tl.custom import Message


class ButtonAction(Enum):
    NEXT_TASK = 1
    SKIP_TASK = 2
    SKIP_BLOCKED_USER = 3


class ReportMessage:
    def __init__(self, message: Message) -> None:
        self.__message = message
        self.__message_body = message.message
        self.__message_items = self.__message_body.split("\n")

    def is_telegram(self) -> bool:
        return "t.me/" in self.__message_body

    def is_joinchat(self) -> bool:
        return "joinchat/" in self.__message_body

    def get_report_reason(self) -> str:
        return self.__message_items[3]

    def get_channel_name(self) -> str:
        if "joinchat/" in self.__message_items[6]:
            return self.__message_items[6].split("joinchat/")[-1]

        name = self.__message_items[6].split("t.me/")[-1]
        if "/" in name:
            name = name.split("/")[0]
        return name

    async def click_button(self, action: ButtonAction) -> None:
        buttons = await self.__message.get_buttons()
        await buttons[action.value][0].click()
