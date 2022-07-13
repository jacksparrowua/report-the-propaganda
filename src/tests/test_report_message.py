# flake8: noqa

from report_message import ReportMessage, decompose_task


class MessageMock:
    def __init__(self, message: str):
        self.message = message


def test_decompose_task():
    t, c, l = decompose_task(
        """Завдання: Виділити пост та додайте скаргу за "Особиста інформація" і додайте текст скарги 👇

🌧 Текст скарги:
Канал розповсюджує фейкові новини та вводить в оман людей!


🔗Посилання: https://t.me/joinchat/Jnng5QoCTLM4MTcy"""
    )

    assert t == 'Виділити пост та додайте скаргу за "Особиста інформація" і додайте текст скарги'
    assert c == "Канал розповсюджує фейкові новини та вводить в оман людей!"
    assert l == "https://t.me/joinchat/Jnng5QoCTLM4MTcy"

    t, c, l = decompose_task(
        """Завдання: Виділити пост та додайте скаргу за "Особиста інформація" і додайте текст скарги 👇

🔗Посилання: https://t.me/joinchat/Jnng5QoCTLM4MTcy"""
    )

    assert t is None
    assert c is None
    assert l is None


def test_report_message_is_telegram():
    mess = MessageMock(
        """Завдання: Виділити пост та додайте скаргу за "Особиста інформація" і додайте текст скарги 👇

🌧 Текст скарги:
Канал розповсюджує фейкові новини та вводить в оман людей!


🔗Посилання: https://t.me/joinchat/Jnng5QoCTLM4MTcy"""
    )

    rm = ReportMessage(mess)
    assert rm.is_telegram() == True
    assert rm.is_joinchat() == True
    assert rm.get_report_reason() == "Канал розповсюджує фейкові новини та вводить в оман людей!"
    assert rm.get_channel_name() == "Jnng5QoCTLM4MTcy"

    mess = MessageMock(
        """Завдання: Виділити пост та додайте скаргу за "Особиста інформація" і додайте текст скарги 👇

🔗Посилання: https://t.me/joinchat/Jnng5QoCTLM4MTcy"""
    )

    rm = ReportMessage(mess)
    assert rm.is_telegram() == False
    assert rm.is_joinchat() == False
    assert rm.get_report_reason() == ""
    assert rm.get_channel_name() == ""
