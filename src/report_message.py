import re
from enum import Enum
from typing import Tuple

from telethon.tl.custom import Message


class ButtonAction(Enum):
    NEXT_TASK = 1
    SKIP_TASK = 2
    SKIP_BLOCKED_USER = 3


_task_pattern = re.compile(r"^Завдання:(.+)👇\W+🌧 Текст скарги:\W+(.+)\W+🔗Посилання:(.+)\W*$")


def decompose_task(task: str) -> Tuple[str, str, str]:
    """Split task to parts - task, complaint and link.

    Args:
        task: string with a task

    Returns:
        Tuple with task, complaint and link.
    """
    # empty string or `None`
    if not task:
        return (None, None, None)

    found = _task_pattern.findall(task)
    found = found[0] if len(found) else found

    if len(found) != 3:
        return (None, None, None)

    task_text, complaint_text, link_text = found

    return task_text.strip(), complaint_text.strip(), link_text.strip()


class ReportMessage:
    def __init__(self, message: Message) -> None:
        # NOTE: message body is in `message.message`
        self.__message = message
        self.task, self.complaint, self.link = decompose_task(message.message)

    def is_telegram(self) -> bool:
        return "t.me/" in self.link

    def is_joinchat(self) -> bool:
        return "joinchat/" in self.link

    def get_report_reason(self) -> str:
        return self.complaint

    def get_channel_name(self) -> str:
        if self.is_joinchat():
            return self.link.split("joinchat/")[-1]

        name = self.link.split("t.me/")[-1]
        if "/" in name:
            name = name.split("/")[0]
        return name

    async def click_button(self, action: ButtonAction) -> None:
        buttons = await self.__message.get_buttons()
        await buttons[action.value][0].click()
