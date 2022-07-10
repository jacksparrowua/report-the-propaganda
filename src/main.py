import asyncio
import os
import random
import time

from telethon import TelegramClient, functions, types

import colors as clr
from misc import get_logger
from report_message import ButtonAction, ReportMessage


LOGGER = get_logger("report the propaganda")
CHANNEL_NAME = "stopdrugsbot"
START_NEW_REPORT_MESSAGE = "🚩Надіслати скаргу на ресурс"
API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]


async def retrieve_report(client: TelegramClient, channel: str, message: str) -> ReportMessage:
    await client.send_message(channel, message)  # start new report task
    time.sleep(round(random.randint(2, 4) + random.uniform(0.0, 1.0), 3))  # wait for the bot response
    last_channel_message = await client.get_messages(channel, from_user=channel, limit=1)
    return ReportMessage(message=last_channel_message[0])


async def process_report(client: TelegramClient, report: ReportMessage, count: int = 0) -> bool:
    is_successfull = False
    if report.is_telegram():
        try:
            channel = report.get_channel_name()
            reason = report.get_report_reason()

            # retrieve channel ID
            if report.is_joinchat():
                request = functions.messages.CheckChatInviteRequest(hash=report.get_channel_name())
                response = await client(request)
                channel_to_be_reported_id = response.chat.id

                _message = (
                    "#{} Reporting channel by invite link {bold}'{}'{end} "
                    "with id {bold}'{}'{end}. "
                    "Reason: {bold}'{}'{end}"
                ).format(
                    count,
                    channel,
                    channel_to_be_reported_id,
                    reason,
                    bold=clr.CBOLD,
                    end=clr.CEND,
                )
            else:
                channel_to_be_reported = await client.get_entity(report.get_channel_name())
                channel_to_be_reported_id = channel_to_be_reported.id

                _message = (
                    "#{} Reporting channel with name {bold}'{}'{end} "
                    "and id {bold}'{}'{end}. "
                    "Reason: {bold}'{}'{end}"
                ).format(
                    count,
                    channel,
                    channel_to_be_reported_id,
                    reason,
                    bold=clr.CBOLD,
                    end=clr.CEND,
                )
            LOGGER.info(_message)

            # reporting
            request = functions.messages.ReportRequest(
                peer="username",
                id=[channel_to_be_reported_id],
                reason=types.InputReportReasonOther(),
                message=report.get_report_reason(),
            )
            response = await client(request)

            if response:
                LOGGER.info(f"{clr.CGREEN}{'Reported.'}{clr.CEND}")
                is_successfull = True
                await report.click_button(ButtonAction.NEXT_TASK)
            else:
                LOGGER.warning(f"{clr.CRED}{'Something went wrong. Skipping the task'}{clr.CEND}")
                await report.click_button(ButtonAction.SKIP_TASK)

        except ValueError as valueError:
            LOGGER.warning(f"{clr.CRED}{str(valueError)}{clr.CEND}")
            if "No user has" in str(valueError):
                await report.click_button(ButtonAction.SKIP_BLOCKED_USER)
            else:
                LOGGER.warning(f"{clr.CRED}{'Something went wrong. Skipping the task'}{clr.CEND}")
                await report.click_button(ButtonAction.SKIP_TASK)
        except Exception as e:
            LOGGER.warning(f"{clr.CRED}{str(e)}{clr.CEND}")
            # if "A wait of" in str(e):
            #     exit()  # spam protection, just wait the time from the message
            await report.click_button(ButtonAction.SKIP_TASK)
            raise
    else:
        LOGGER.info(f"{clr.CYELLOW}{'Skipping task, no telegram link in the description'}{clr.CEND}")
        await report.click_button(ButtonAction.SKIP_TASK)

    return is_successfull


async def main() -> None:
    """Report entrypoint.

    To run this script you need to setup `API_ID` and `API_HASH` env variables.
    To get more info how to create then use official Telegram docs - https://my.telegram.org/apps
    """
    successfull_cnt = 0
    total_cnt = 0

    def stats():
        return f"Reported {successfull_cnt} channels. Total number of reports is {total_cnt}."

    async with TelegramClient("session_name", API_ID, API_HASH) as client:
        try:
            while True:
                report = await retrieve_report(client, CHANNEL_NAME, START_NEW_REPORT_MESSAGE)

                is_successfull = await process_report(client, report, successfull_cnt)
                successfull_cnt += int(is_successfull)
                total_cnt += 1

                # wait some time to prevent spam protection
                delay = random.randint(30, 35) if is_successfull else random.randint(10, 15)
                delay += random.uniform(0.0, 2.0)
                delay = round(delay, 3)
                LOGGER.info(f"Waiting {clr.CBLUE}{delay}{clr.CEND} seconds...")
                time.sleep(delay)

        except KeyboardInterrupt:
            LOGGER.info("Interrupting report session.")
            LOGGER.info(stats())
        except Exception as e:
            LOGGER.warning("Got an exception: " + str(e))
            LOGGER.info(stats())


if __name__ == "__main__":
    asyncio.run(main())
