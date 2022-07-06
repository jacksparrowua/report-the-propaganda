import random

from report_message import ButtonAction, ReportMessage

try:
    import colorama

    colorama.init()
except ImportError:
    raise

import asyncio
import time

from colorama import Fore
from telethon import TelegramClient, functions, types

from config import api_hash, api_id

channel_name = "stopdrugsbot"
start_new_report_message = "🚩Надіслати скаргу на ресурс"


async def main():
    count = 0
    client = TelegramClient("session_name", api_id, api_hash)
    await client.start()

    while True:
        # wait some time to prevent spam protection
        delay = random.randint(20, 45) + random.uniform(0.0, 2.0)
        print(f"Waiting {delay} seconds...")
        time.sleep(delay)

        await client.send_message(channel_name, start_new_report_message)  # start new report task
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


asyncio.run(main())

if __name__ == "__main__":
    main()
