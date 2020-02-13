import telebot


bot = telebot.TeleBot("940199210:AAHEpa7bUH5eLpRu-VZQ5ENg2F-ga-Ft3Ns")


@bot.message_handler(content_types=["document"])
def start_doc(message):
    if str(message.from_user.username) == "None":
        if "py" in message.document.file_name:
            bot.delete_message(message.chat.id,message.message_id)
            bot.send_message(message.chat.id, text="Уважаемый {}! \n\nПожалуйста, заливаёте ваши исходные коды на сервисы: pastebin.com или gist.github.com \n\nСпасибо за понимания!".format(message.from_user.first_name), reply_to_message_id=message.message_id)
    else:
        if "py" in message.document.file_name:
            bot.delete_message(message.chat.id,message.message_id)
            bot.send_message(message.chat.id, text="Уважаемый @{}! \n\nПожалуйста, заливаёте ваши исходные коды на сервисы: pastebin.com или gist.github.com \n\nСпасибо за понимания!".format(message.from_user.username))


bot.polling(none_stop=True)

