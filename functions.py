import csv
from telegram.ext import Updater, CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from constans import *
from stickersi import *
import random


def read_csv():
    with open("victorina/database.csv", encoding="utf-8") as file:
        read_data = list(csv.reader(file, delimiter="|", lineterminator="\n"))
        return read_data


def write_to_csv(row):
    with open("victorina/database.csv",mode="a", encoding="utf-8") as file:
        writter = csv.writer(file, delimiter="|", lineterminator="\n")
        writter.writerow(row)
        
def start(update:Update, context:CallbackContext):
    keyboard = [[GO]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_sticker(START_STIC[1])
    context.bot.send_message(update.effective_chat.id, "Добро пожаловать в викторину. Отвечайна вопросы, выбирая один из вариантов ответа ")
    update.message.reply_text(f"Для начала нажми на {GO}", reply_markup=markup)
    
    questions_list = read_csv()
    random.shuffle(questions_list)
    length = QUESTIONS_ON_ROUND if len(questions_list) > QUESTIONS_ON_ROUND else len(questions_list)
    
    questions_list = questions_list[:length]
    context.user_data["questions"] = questions_list
    context.user_data["index"] = 0
    context.user_data["counter"] = 0
    return GAME

def cancel(update:Updater, context:CallbackContext):
    update.message.reply_sticker(START_STIC[0])
    update.message.reply_text("Спасибо за участие!")
    update.message.reply_text("Нажми на /start, чтобы начать заново")
    return ConversationHandler.END
    
    
def game(update:Updater, context:CallbackContext):
    questions_list = context.user_data["questions"]    
    index = context.user_data["index"]
    if "right_answers" in context.user_data:
        right_answer = context.user_data["right_answers"]
        my_answer = update.message.text
        if right_answer == my_answer:
            context.user_data["counter"] += 1
            update.message.reply_photo(RIGHT_IMG)
            update.message.reply_text("Правильно!")
        else:
            update.message.reply_photo(WRONG_IMG)
            update.message.reply_text("Неправильно!")
    try:
        
        answers = questions_list[index] #ответы
        question = answers.pop(0) #вопросы
        right_answer = answers[1]
        random.shuffle(answers)
        # print(questions_list)
        # print(f"{question=}")
        # print(f"{answers=}")
        
        keyboard = [answers[2:],answers[:2]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text(question, reply_markup=markup)
        
        context.user_data["index"] += 1
        context.user_data["right_answers"] = right_answer
    except IndexError:
        counter = context.user_data["counter"]
        counter_questions = len(questions_list)
        update.message.reply_text(f"Правильных ответов: {counter}/{counter_questions}", reply_markup=ReplyKeyboardRemove())
        if counter <=1:
            update.message.reply_text("Ты можешь лучше!")
        elif counter <=2:
            update.message.reply_text("Неплохо")
        elif counter <=3:
            update.message.reply_text("Хороший результат!")
        elif counter <=4:
            update.message.reply_photo("https://img2.freepng.ru/20180528/jkb/kisspng-pixel-art-art-museum-youtube-win-win-5b0c48f6826a62.3314939715275317665342.jpg")
            update.message.reply_text("Отлично! Ты победил!!")
        del context.user_data["right_answers"]    
        return ConversationHandler.END
        