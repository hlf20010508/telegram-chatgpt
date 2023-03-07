import os
import io
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from log import logger
from chatgpt import ChatGPT
from ogg_to_wav import convert


# telegram
TOKEN = os.environ['token']
# openai
api_key = os.environ['api_key']
model = os.environ.get('model', 'gpt-3.5-turbo')
preset = os.environ.get('preset', '')
memory_length = int(os.environ.get('memory_length', 100))

help_text = """
Here are commands for you:
- `/start` to start with bot
- `/forget` to remove all memory
- `/reset A SENTENCE ABOUT BOT'S CHARACTER` to reset character background
"""

start_text = """
Hey there! I'm a chat bot based on chatgpt.
Feel free to talk with me.
`/help` for help.
"""

chatgpt = ChatGPT(api_key, model, preset, memory_length)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger('User %s started a conversation.\n'%chat_id)
    await context.bot.send_message(chat_id=chat_id, text=start_text)

async def forget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chatgpt.delete_memory()
    logger("User %s removed bot's memory.\n"%chat_id)
    await context.bot.send_message(chat_id=chat_id, text="Memory removed.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    setting = ' '.join(context.args)
    old_setting = chatgpt.preset
    chatgpt.reset_character(setting)
    logger("User %s reset bot's character\nfrom:\n%s\nto:\n%s\n"%(chat_id, old_setting, setting))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Successfully reset bot's character\nfrom:\n%s\nto:\n%s\n"%(old_setting, setting))

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger('User %s requested help.\n'%chat_id)
    await context.bot.send_message(chat_id=chat_id, text=help_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    content = update.message.text
    reply = chatgpt.reply(content)
    logger('User %s: %s\nBot: %s\n'%(chat_id, content, reply))
    await context.bot.send_message(chat_id=chat_id, text=reply)

async def voice(update: Update, context: ContextTypes().DEFAULT_TYPE):
    # output is .webm file
    chat_id = update.effective_chat.id
    content = update.message.voice
    voice_file = await content.get_file()
    await voice_file.download_to_drive('voice.oga')
    convert('voice.oga', 'voice.wav')
    with open('voice.wav', 'rb') as voice_file:
        voice_text = chatgpt.voice_detect(voice_file)['text']
        os.remove('voice.oga')
        os.remove('voice.wav')
    reply = chatgpt.reply(voice_text)
    logger('(Voice) User %s: %s\nBot: %s\n'%(chat_id, voice_text, reply))
    await context.bot.send_message(chat_id=chat_id, text=reply)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    forget_handler = CommandHandler('forget', forget)
    reset_handler = CommandHandler('reset', reset)
    help_handler = CommandHandler('help', help)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    voice_handler = MessageHandler(filters.VOICE, voice)

    application.add_handler(start_handler)
    application.add_handler(forget_handler)
    application.add_handler(reset_handler)
    application.add_handler(help_handler)
    application.add_handler(echo_handler)
    application.add_handler(voice_handler)
    
    application.run_polling()