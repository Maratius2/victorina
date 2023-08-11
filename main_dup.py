from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, CommandHandler
from telegram.ext.filters import Filters
from config import TOKEN
from functions import *



#Сам бот и его зам.
updater = Updater(TOKEN)
dispatcher = updater.dispatcher


contact_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
            GAME: [MessageHandler(Filters.text & ~Filters.command, game)]
        },
    fallbacks=[CommandHandler("cancel", cancel)]
)


dispatcher.add_handler(contact_handler)



print("server started")
updater.start_polling()
updater.idle()
