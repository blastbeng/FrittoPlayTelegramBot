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
            context.bot.send_message(chat_id=update.effective_chat.id, text="si è verificato un errore stronzo", disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="se vuoi dirmi o chiedermi qualcosa devi scrivere una frase dopo /ask", disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        
ask_handler = CommandHandler('ask', ask)
dispatcher.add_handler(ask_handler)

def search(update: Update, context: CallbackContext):
    strid = str(update.effective_chat.id)
    message = update.message.text[8:].strip();
    if(message != "" and (CHAT_ID == strid or GROUP_CHAT_ID == strid)):
        url = API_URL + API_PATH_TEXT + "search/" + message

        response = requests.get(url)
        if (response.text != "Internal Server Error"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=response.text, disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="si è verificato un errore stronzo", disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="se vuoi che cerco qualcosa devi scrivere una frase dopo /search", disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        
ask_handler = CommandHandler('search', search)
dispatcher.add_handler(ask_handler)



def insult(update: Update, context: CallbackContext):
    strid = str(update.effective_chat.id)
    message = update.message.text[8:].strip();
    if(CHAT_ID == strid or GROUP_CHAT_ID == strid):
        if message != "":
            url = API_URL + API_PATH_TEXT + "insult?text=" + message
        else:
            url = API_URL + API_PATH_TEXT + "insult"

        response = requests.get(url)
        if (response.text != "Internal Server Error"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=response.text[1:-1], disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="si è verificato un errore stronzo", disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
            
ask_handler = CommandHandler('insult', insult)
dispatcher.add_handler(ask_handler)





def help(update: Update, context: CallbackContext):

    text = "/ask - chiedi qualcosa al bot\n" + "/insult - insulta qualcuno o qualcosa\n" + "/search - cerca qualcosa su wikipedia\n" + "/help - visualizza i comandi disponibili";

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
           
ask_handler = CommandHandler('help', help)
dispatcher.add_handler(ask_handler)

#def echo(update: Update, context: CallbackContext):
#    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

#echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
#dispatcher.add_handler(echo_handler)

updater.start_polling()