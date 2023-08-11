import csv
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from config import TOKEN


def read_csv():
    with open("victorina/database.csv", encoding="utf-8") as file:
        read_data = list(csv.reader(file, delimiter="|"))
        return read_data


def write_to_csv(row):
    with open("victorina/database.csv",mode="a", encoding="utf-8") as file:
        writter = csv.writer(file, delimiter="|", lineterminator="\n")
        writter.writerow(row)
        
        
print(read_csv())    
write_to_csv(row=["У какой роли из нижеперечисленного списка есть доступ к люку (игра Among us)",
                       "Инженер", "Ученый", "Призрак", "Ангел-хранитель"])