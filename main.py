import telebot
import os
from flask import Flask, request


TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")
server = Flask(__name__)
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=["document"])
def start_doc(message):
    if message.document.file_name.endswith("py"):
        try:
            bot.send_message(message.chat.id, text="Уважаемый @{} ! \n\nПожалуйста, заливайте ваши исходные коды на сервисы: pastebin.com или gist.github.com \n\nСпасибо за понимания!".format(user_mention(message.from_user)))
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as A:
            print("[LOG]", A)


def user_mention(user):
    return user.username if user.username else user.first_name


@bot.message_handler(commands=["check"])
def check_status(message):
    bot.send_message(message.chat.id, "Ok!", reply_to_message_id=message.message_id)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))