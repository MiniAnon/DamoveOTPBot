from config import *
import telebot
import openai
chatStr = '' 
def ChatModal(prompt):
    global chatStr
    openai.api_key=OPENAI_KEY
    chatStr += f"Damove: {prompt}\nDamoveBot: "
    response = openai.completions.create(
                model="davinci-002",
                prompt=chatStr,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
    chatStr += f"{response['choices'][0]['text']}"
    return response['choices'][0]['text']
bot=telebot.TeleBot(BOT_API)
@bot.message_handler(['start'])
def start(message):
    bot.reply_to(message,"Hello,  Welcome to Damove OTP Bypass Bot")
@bot.message_handler()
def chat(message):
    #if message.from_user.id==my_id:
        try:
            reply = ChatModal(message.text)
            bot.reply_to(message,reply)
        except Exception as e:
            print(e)
            bot.reply_to(message,e)
    # else:
    #     print("Someone else tried our bot: ",message.text)
print("Bot Started...")
bot.polling()