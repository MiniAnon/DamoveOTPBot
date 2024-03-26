import asyncio
import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from twilio.rest import Client

# Replace with your Twilio credentials, Telegram bot token, and TwiML Bin URL
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
twiml_bin_url = "https://www.twilio.com/docs/serverless/twiml-bins"  # Replace with your actual URL

client = Client(account_sid, auth_token)


async def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! I can make calls and initiate OTP verification (with user input).")


async def call(update: Update, context: CallbackContext):
    message = update.message
    phone_number_to_call = message.text.split()[1]  # Extract phone number from message

    # Explicitly inform the user about the purpose of calling and OTP capture
    await context.bot.send_message(
        chat_id=message.chat_id,
        text="To verify your identity, I'll call the number provided and the recipient will receive an OTP. Please ask the recipient to enter the OTP here when prompted.",
    )

    try:
        call = await client.calls.create(
            url=twiml_bin_url,
            to=phone_number_to_call,
            from_=twilio_phone_number
        )
        await context.bot.send_message(chat_id=message.chat_id, text="Calling...")

        # **Prompt user for OTP:**
        await context.bot.send_message(
            chat_id=message.chat_id,
            text="Please ask the recipient to enter the OTP they receive on their phone here."
        )

        # **Handle user input for OTP (no direct capture):**
        # ... (Implement logic using MessageHandler to receive user's entered OTP)
    except Exception as e:
        await context.bot.send_message(chat_id=message.chat_id, text="Error: " + str(e))


async def handle_otp_input(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    entered_otp = update.message.text  # Extract user-entered OTP

    # **Send the entered OTP to your server securely (no storage here):**
    # ... (Implement logic to send the entered OTP to your server for verification)

    verification_response = "**Placeholder for verification response from server**"  # Replace with actual response

    await context.bot.send_message(chat_id=chat_id, text=verification_response)


async def main():
    logging.basicConfig(level=logging.INFO)

    updater = Updater(telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("call", call))
    dispatcher.add_handler(MessageHandler(Filters.Text, handle_otp_input))  # Handle user's entered OTP

    await updater.start_polling()
    await updater.idle()


if __name__ == "__main__":
    asyncio.run(main())
