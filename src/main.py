import asyncio
import os
import random
import time

try:
    import colorama

    colorama.init()
except ImportError:
    raise


from colorama import Fore
from telethon import TelegramClient, functions, types

from report_message import ButtonAction, ReportMessage

channel_name = "stopdrugsbot"
start_new_report_message = "🚩Надіслати скаргу на ресурс"


API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]


async def main() -> None:
    """Report entrypoint.
    To run this script you need to setup `API_ID` and `API_HASH` env variables.
    To get more info how to create then use official Telegram docs - https://my.telegram.org/apps
    """
    count = 0
    client = TelegramClient("session_name", API_ID, API_HASH)
    await client.start()

    while True:
        # wait some time to prevent spam protection
        delay = random.randint(20, 35) + random.uniform(0.0, 2.0)
        print(f"Waiting {delay} seconds...")
        time.sleep(delay)

        await client.send_message(channel_name, start_new_report_message)  # start new report task
        time.sleep(random.randint(2, 4) + random.uniform(0.0, 1.0))  # wait for bot response
        last_channel_message = await client.get_messages(channel_name, limit=1)
        report = ReportMessage(message=last_channel_message[0])

        if report.is_telegram():
            try:
                if report.is_joinchat():
                    request = functions.messages.CheckChatInviteRequest(hash=report.get_channel_name())
                    response = await client(request)
                    channel_to_be_reported_id = response.chat.id

                    print(
                        "#{} Reporting channel by invite link {} with id {}. Reason: {}".format(
                            count, report.get_channel_name(), channel_to_be_reported_id, report.get_report_reason()
                        )
                    )
                else:
                    channel_to_be_reported = await client.get_entity(report.get_channel_name())
                    channel_to_be_reported_id = channel_to_be_reported.id

                    print(
                        "#{} Reporting channel with name {} and id {}. Reason: {}".format(
                            count, report.get_channel_name(), channel_to_be_reported_id, report.get_report_reason()
                        )
                    )

                request = functions.messages.ReportRequest(
                    peer="username",
                    id=[channel_to_be_reported_id],
                    reason=types.InputReportReasonOther(),
                    message=report.get_report_reason(),
                )

                response = await client(request)

                if response:
                    print(f"{Fore.LIGHTGREEN_EX}{'Reported.'}{Fore.RESET}")
                    count += 1
                    await report.click_button(ButtonAction.NEXT_TASK)
                else:
                    print(f"{Fore.LIGHTRED_EX}{'Something went wrong. Skipping the task'}{Fore.RESET}")
                    await report.click_button(ButtonAction.SKIP_TASK)
            except ValueError as valueError:
                print(f"{Fore.LIGHTRED_EX}{str(valueError)}{Fore.RESET}")
                if "No user has" in str(valueError):
                    await report.click_button(ButtonAction.SKIP_BLOCKED_USER)
                else:
                    print(f"{Fore.LIGHTRED_EX}{'Something went wrong. Skipping the task'}{Fore.RESET}")
                    await report.click_button(ButtonAction.SKIP_TASK)
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}{str(e)}{Fore.RESET}")
                if "A wait of" in str(e):
                    exit()  # spam protection, just wait the time from the message
                await report.click_button(ButtonAction.SKIP_TASK)
        else:
            print(f"{Fore.LIGHTYELLOW_EX}{'Skipping task, no telegram link in the description'}{Fore.RESET}")
            await report.click_button(ButtonAction.SKIP_TASK)


if __name__ == "__main__":
    asyncio.run(main())
