import asyncio
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, Filters
from twilio.rest import Client

# Replace with your Twilio credentials and Telegram bot token
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! I can make calls. Send me a command like /call <phone_number> to initiate a call.")


async def make_call(update: Update, context: CallbackContext):
    message = update.message
    phone_number = message.text.split()[1]  # Extract phone number from message

    try:
        client = Client(account_sid, auth_token)
        call = await client.calls.create(
            url="https://www.twilio.com/docs/serverless/twiml-bins",  # Replace with your TwiML Bin URL
            to=phone_number,
            from_=twilio_phone_number
        )
        await context.bot.send_message(chat_id=message.chat_id, text="Calling...")
    except Exception as e:
        await context.bot.send_message(chat_id=message.chat_id, text="Error: " + str(e))


async def main():
    logging.basicConfig(level=logging.INFO)

    updater = Updater(telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("call", make_call))

    await updater.start_polling()
    await updater.idle()


if __name__ == "__main__":
    asyncio.run(main())
