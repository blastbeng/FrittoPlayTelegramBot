import asyncio
import telegram
import logging
import os
import json
import requests
import time
import sys
from datetime import datetime, timedelta
from os.path import join, dirname
from dotenv import load_dotenv
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CommandHandler, Dispatcher
from telegram import Update
from pytz import timezone


load_dotenv()


TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")
API_URL = os.environ.get("API_URL")
API_PATH_TEXT = os.environ.get("API_PATH_TEXT")
API_PATH_JOKES_TEXT = os.environ.get("API_PATH_JOKES_TEXT")

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
    if((CHAT_ID == strid or GROUP_CHAT_ID == strid)):
        message = update.message.text[5:].strip();
        if(message != ""):
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




def chuck(update: Update, context: CallbackContext):
    strid = str(update.effective_chat.id)
    if(CHAT_ID == strid or GROUP_CHAT_ID == strid):
        url = API_URL + API_PATH_JOKES_TEXT + "chuck"

        response = requests.get(url)
        if (response.text != "Internal Server Error"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=response.text, disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="si è verificato un errore stronzo", disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        
ask_handler = CommandHandler('chuck', chuck)
dispatcher.add_handler(ask_handler)




def joke(update: Update, context: CallbackContext):
    strid = str(update.effective_chat.id)
    if(CHAT_ID == strid or GROUP_CHAT_ID == strid):
        url = API_URL + API_PATH_JOKES_TEXT + "random"

        response = requests.get(url)
        if (response.text != "Internal Server Error"):
            context.bot.send_message(chat_id=update.effective_chat.id, text=response.text, disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="si è verificato un errore stronzo", disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        
ask_handler = CommandHandler('joke', joke)
dispatcher.add_handler(ask_handler)

def search(update: Update, context: CallbackContext):
    strid = str(update.effective_chat.id)
    if((CHAT_ID == strid or GROUP_CHAT_ID == strid)):
        message = update.message.text[8:].strip();
        if(message != ""):
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
            text = response.text.replace('"','')
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="si è verificato un errore stronzo", disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
            
ask_handler = CommandHandler('insult', insult)
dispatcher.add_handler(ask_handler)


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    text = " ⏰ " +  context.job.name + " ⏰"
    context.bot.send_message(job.context, text="⏰ RING RING RING ⏰")
    context.bot.send_message(job.context, text=text)

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        text = ""

        for i in range(len(context.args)):
            if i > 1:
                text = text + " " + context.args[i]

        text = text.strip()

        if text == "":
            update.message.reply_text('Usage: /setalarm <dd-mm> <HH:MM> <text>', disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
            return

        tz = timezone('Europe/Rome')
        now = datetime.now(tz = tz).replace(second=0, microsecond=0)
        time = now.strftime("%Y") + "-" + context.args[0] +  " " + context.args[1] + ":00"


        alarm_time = datetime.strptime(time, "%Y-%d-%m %H:%M:%S")
        current_time = datetime.strptime(now.strftime("%Y-%d-%m %H:%M:%S"), "%Y-%d-%m %H:%M:%S")

        due = alarm_time - current_time
        
        if due.seconds <= 0 or due.days <=-1:
            update.message.reply_text('Devi impostare una data futura.', disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
            return

        job_removed = remove_job_if_exists(text, context)
        context.job_queue.run_once(alarm, due, context=chat_id, name=text)

        text = 'Allarme impostato correttamente!'
        if job_removed:
            text += ' Vecchio allarme rimosso.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /setalarm <dd-mm> <HH:MM> <text>', disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    try:
        text = ""
        
        for i in range(len(context.args)):
            text = text + " " + context.args[i]
        text = text.strip()

        if text == "":
            update.message.reply_text('Usage: /unsetalarm <text>', disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
            return

        job_removed = remove_job_if_exists(text, context)
        text = 'Allarme rimosso correttamente!' if job_removed else 'Nessun allarme attivo.'
        update.message.reply_text(text, disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /unsetalarm <text>', disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)



dispatcher.add_handler(CommandHandler("setalarm", set_timer))
dispatcher.add_handler(CommandHandler("unsetalarm", unset))

def restart(update: Update, context: CallbackContext):


    text = "Riavvio in corso..."
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)

    python = sys.executable
    os.execl(python, python, *sys.argv)

ask_handler = CommandHandler('restart', restart)
dispatcher.add_handler(ask_handler)

def help(update: Update, context: CallbackContext):

    text = "/ask <text> - chiedi qualcosa al bot\n" 
    + "/insult <text> - insulta qualcuno o qualcosa\n" 
    + "/search <text> - cerca qualcosa su wikipedia\n" 
    + "/chuck - Chuck Norris.\n" 
    + "/joke - Barzelletta a caso\n" 
    + "/setalarm <dd-mm> <HH:MM> <text> - imposta un allarme\n" 
    + "/unsetalarm <text> - rimuove un allarme\n" 
    + "/restart - riavvia il bot\n" 
    + "/help - visualizza i comandi disponibili";

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, disable_notification=True, reply_to_message_id=update.message.message_id, protect_content=True)
           
ask_handler = CommandHandler('help', help)
dispatcher.add_handler(ask_handler)

#def echo(update: Update, context: CallbackContext):
#    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

#echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
#dispatcher.add_handler(echo_handler)

updater.start_polling()