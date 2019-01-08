import os
from models import *
import telebot
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")


session = Session()
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))

# input = raw_input("promt")

def send_message(chat_id, message):
    print('Sending message to chat %s, message: %s' % (chat_id, message))


# @bot.message_handler()
# def message_handler(message):
#     # save Info(name=message.text, chat_id=message.chat.id
#     dbworker.set_state(message.chat.id, config.States.S_ENTER_AGE.value)
#     info = Info()
#     info.name = message.text
#     info.chat_id = message.chat.id
#     session.add(info)
#     session.commit()

def start(chat_id):
    user = User()
    user.chat_id = chat_id
    user.stage = session.query(Question).first().id
    session.add(user)
    session.commit()
    bot.send_message(chat_id, session.query(Question).filter_by(id=user.stage).first().text)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    start(message.chat.id)

@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    user = session.query(User).filter_by(chat_id=message.chat.id).first()
    user.stage = session.query(Question).first().id
    answers = session.query(Answer).filter_by(user_id=user.id).delete()
    # session.delete(answers)

    session.add(user)
    session.commit()
    bot.send_message(message.chat.id, session.query(Question).filter_by(id=user.stage).first().text)


@bot.message_handler()
def user_message(message):
    user = session.query(User).filter_by(chat_id=message.chat.id).first()
    if(not user):
        start(message.chat.id)
    else:
        ans = Answer()
        ans.text = message.text
        ans.user_id = user.id
        ans.question_id = user.stage
        session.add(ans)
        session.commit()
        next = session.query(Question).filter(Question.id > user.stage).first()
        if(not next):
            bot.send_message(message.chat.id, "Thank you! We will call you later")
        bot.send_message(message.chat.id, next.text)
        user.stage = next.id
        session.add(user)
        session.commit()

# ans = session.query(Answer).filter_by(chat_id=1).first()
# print(ans)
# # print(dir(query))
#
# if(not ans):
#     question = session.query(Question).first()
#     send_message(1, question.text)
bot.polling()


# info.mail = message.text
# session.add(info)
# session.commit()



# send_message(1, "asd")
