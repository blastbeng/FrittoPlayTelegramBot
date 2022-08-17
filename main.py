import asyncio
import telegram
import logging
import os
import json
import requests
from os.path import join, dirname
from dotenv import load_dotenv
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CommandHandler, Dispatcher
from telegram import Update

load_dotenv()


TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")
API_URL = os.environ.get("API_URL")
API_PATH_TEXT = os.environ.get("API_PATH_TEXT")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

#def start(update: Update, context: CallbackContext):
#    strid = str(update.effective_chat.id)
#    if(CHAT_ID == strid):
#        context.bot.send_message(chat_id=update.effective_chat.id, text="Eccomi qua!")

#start_handler = CommandHandler('start', start)
#dispatcher.add_handler(start_handler)


def ask(update: Update, context: CallbackContext):
    strid = str(update.effective_chat.id)
    message = update.message.text[5:].strip();
    if(message != "" and (CHAT_ID == strid or GROUP_CHAT_ID == strid)):
        url = API_URL + API_PATH_TEXT + "ask/" + message

        response = requests.get(url)
        if (response.text != "Internal Server Error"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=response.text, disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        else:
            context.bot.delete_message(chat_id=strid, message_id=update.message.message_id)
    else:
        context.bot.delete_message(chat_id=strid, message_id=update.message.message_id)

ask_handler = CommandHandler('ask', ask)
dispatcher.add_handler(ask_handler)

#def echo(update: Update, context: CallbackContext):
#    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

#echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
#dispatcher.add_handler(echo_handler)

updater.start_polling()