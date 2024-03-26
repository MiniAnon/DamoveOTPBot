from aiogram import Bot, Dispatcher, types
import logging
import asyncio
from twilio.rest import Client

# Telegram bot token (replace 'YOUR_TOKEN' with your bot's token)
telegram_bot_token = '6761737569:AAHvKsm-GVVlGyybypaNCukUkBr__iCpomI'

# Twilio credentials
account_sid = 'AC9990f72bbc21f4b81ecf66f2fd095613'
auth_token = 'f1c3d1c205a2fb5f6c39d29831ac0766'
twilio_phone_number = '+18336587998'

# Create bot and dispatcher instances
bot = Bot(token=telegram_bot_token)
dp = Dispatcher(bot)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define a command handler to start the call
@dp.message_handler(commands=['start_call'])
async def start_call(message: types.Message):
    await message.reply("Please enter the victim's phone number:")
    # Register the next handler to receive the victim's phone number
    dp.register_message_handler(get_victim_number, state='get_number')

# Define a handler to receive the victim's phone number
async def get_victim_number(message: types.Message):
    victim_number = message.text
    await message.reply(f"Calling victim at {victim_number}...")

    # Make the call using Twilio
    client = Client(account_sid, auth_token)
    try:
        call = client.calls.create(
            to=victim_number,
            from_=twilio_phone_number,
            twiml='<Response><Say>Hello, you are receiving a call from the Telegram bot!</Say></Response>'
        )
        await message.reply(f"Call SID: {call.sid}")
    except Exception as e:
        await message.reply(f"Error making call: {str(e)}")

    # Unregister the handler
    dp.unregister_message_handler(get_victim_number, state='get_number')

# Start the bot
if __name__ == '__main__':
    asyncio.run(dp.start_polling())