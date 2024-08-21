import json
import time

from telebot import TeleBot, types

from translate import to_latin, to_cyrillic
import requests
import os
# from database import cursor, db
import sqlite3 as sql
db = sql.connect("database.db", check_same_thread=False)
cursor = db.cursor()
from utils import create_json_file

#shuyerdan

bot_token = '6825083256:AAECqqQd6aZHXa63QBcuATu9qx7DD07KBpc'
api_url = f'https://api.telegram.org/bot{bot_token}/deleteWebhook'

# Send the request to delete the webhook
response = requests.post(api_url)

# Check if the request was successful
if response.status_code == 200:
    print("Webhook deleted successfully.")
else:
    print(f"Failed to delete webhook. Status code: {response.status_code}")
    print(response.text)
#shuyergacha webhookni delete qilish uchun ishlatildi.


token = '6825083256:AAECqqQd6aZHXa63QBcuATu9qx7DD07KBpc'
bot = TeleBot(token)


@bot.message_handler(commands=['messages'])
def exact_user(message: types.Message):
    chat_id = message.chat.id

    if int(chat_id) != 6956376313:
        msg = "Siz admin emasligingiz tufayli, bu huquqdan foydalana olmaysiz!🚫"
        bot.send_message(message.chat.id, msg)
        bot.delete_message(chat_id=chat_id, message_id=message.id)
        return
    else:
        bot.send_message(message.chat.id, "Barcha foydalanuvchilar uchun xabarni kiriting: ")

        # bu yerda message - foydalanuvchi kiritgan textga teng, uni keyin send_message_to_user funksiyaga berib yuboradi
        bot.register_next_step_handler(message, send_message_to_users)

def send_message_to_users(message: types.Message):
    message_content = f"==== ADMIN ====\n\n{message.text}"
    users = cursor.execute("SELECT user_id FROM user").fetchall()
    print(users)
    for user in users:
        bot.send_message(user[0], message_content)
    bot.send_message(message.chat.id, "Xabar muvaffaqiyatli yuborildi✅")


@bot.message_handler(commands=['message'])
def exact_user(message: types.Message):
    chat_id = message.chat.id

    if int(chat_id) != 6956376313:
        msg = "Siz admin emasligingiz tufayli, bu huquqdan foydalana olmaysiz!🚫"
        bot.send_message(message.chat.id, msg)
        bot.delete_message(chat_id=chat_id, message_id=message.id)
        return
    else:
        bot.send_message(message.chat.id, "User ID-sini kiriting: ")

        # bu yerda message - foydalanuvchi kiritgan textga teng, uni keyin send_message_to_user funksiyaga berib yuboradi
        bot.register_next_step_handler(message, id_definer)


def id_definer(message: types.Message):
    try:
        message_content = int(message.text)
        user = cursor.execute("SELECT user_id FROM user where id = ?", (message_content,)).fetchone()

        if user:
            bot.send_message(message.chat.id, "Xabarni kiriting: ")
            bot.register_next_step_handler(message, message_sender, user[0])
        else:
            bot.send_message(message.chat.id, "Kiritilgan ID mavjud emas!❌")
    except ValueError:
        bot.send_message(message.chat.id, "Faqat ID(raqam) kiriting!❌")

def message_sender(message: types.Message, user):
    aka = f"==== ADMIN ====\n\n{message.text}"
    bot.send_message(user, aka)
    bot.send_message(message.chat.id, "Xabar muvaffaqiyatli yuborildi✅")


@bot.message_handler(commands=['pins'])
def pin_message(message: types.Message):
    chat_id = message.chat.id

    if int(chat_id) != 6956376313:
        msg = "Siz admin emasligingiz tufayli, bu huquqdan foydalana olmaysiz!🚫"
        bot.send_message(message.chat.id, msg)
        bot.delete_message(chat_id=chat_id, message_id=message.id)
        return
    else:
        bot.send_message(message.chat.id, "PINda turishi kerak bo'lgan matnni kiriting: ")
        bot.register_next_step_handler(message, pin_text_to_all_users)


def pin_text_to_all_users(message: types.Message):
    text_to_pin = f"📌PIN: {message.text}"
    users = cursor.execute("SELECT user_id, first_name, username, id FROM user").fetchall()
    count = 0
    for user_id in users:
        try:
            x = bot.send_message(user_id[0], text_to_pin)
            bot.pin_chat_message(user_id[0], x.message_id)
        except Exception as e:
            count += 1
            bot.send_message(message.chat.id, f"Bunday foydalanuvchi mavjud emas!🚫\n[{user_id[3]}] 👉 [{user_id[1]}] 👉 [@{user_id[2]}]")
    bot.send_message(message.chat.id, f"{count} ta foydalanuvchi botni tark etibdi🙅‍♂️\n\nXabar barcha foydalanuvchilar uchun muvaffaqiyatli PINga o'rnatildi!✅")


# @bot.message_handler(commands=['unactives'])
# def unactive_users(message: types.Message):
#     users = cursor.execute("SELECT user_id, first_name, username, id FROM user").fetchall()
#     count=0
#     for user_id in users:
#         try:
#             bot.send_message(user_id[0], "")
#         except Exception as e:
#             count+=1
#             bot.send_message(message.chat.id, f"Bunday foydalanuvchi mavjud emas!🚫\n[{user_id[3]}] 👉 [{user_id[1]}] 👉 [@{user_id[2]}]")
#     bot.send_message(message.chat.id, f"{count} ta foydalanuvchi botni tark etibdi🙅‍♂️")



@bot.message_handler(commands=['unpins'])
def unpin_message(message: types.Message):
    chat_id = message.chat.id

    if int(chat_id) != 6956376313:
        msg = "Siz admin emasligingiz tufayli, bu huquqdan foydalana olmaysiz!🚫"
        bot.send_message(message.chat.id, msg)
        bot.delete_message(chat_id=chat_id, message_id=message.id)
        return
    else:
        users = cursor.execute("SELECT user_id FROM user").fetchall()
        for user_id in users:
            try:
                bot.unpin_chat_message(user_id[0])
            except Exception as e:
                print(f"Ushbu foydalanuvchi uchun ishlamadi {user_id[0]}: {str(e)}")
        bot.send_message(message.chat.id, "Xabar muvaffaqiyatli PINdan olib tashlandi✅")



#aynan 1 ta user uchun pin
@bot.message_handler(commands=['pin'])
def pin_message_for_user(message: types.Message):
    chat_id = message.chat.id

    if int(chat_id) != 6956376313:
        msg = "Siz admin emasligingiz tufayli, bu huquqdan foydalana olmaysiz!🚫"
        bot.send_message(message.chat.id, msg)
        bot.delete_message(chat_id=chat_id, message_id=message.id)
        return
    else:
        bot.send_message(message.chat.id, "PINda turishi kerak bo'lgan user IDsini kiriting: ")
        bot.register_next_step_handler(message, get_user_id_and_pin_message)


def get_user_id_and_pin_message(message: types.Message):
    try:
        user_id = int(message.text)
        user = cursor.execute("select user_id from user where id = ?", (user_id,)).fetchone()
        if user:
            bot.send_message(message.chat.id, "Foydalanuvchida PINda chiqib turishi kerak bo`lgan xabarni kiriting: ")
            bot.register_next_step_handler(message, send_and_pin_message, user[0])
        else:
            bot.send_message(message.chat.id, "Mavjud bo`lmagan ID kiritdingiz!")
    except ValueError:
        bot.send_message(message.chat.id, "Faqat ID(raqam) kirita olasiz!🚫")


def send_and_pin_message(message: types.Message, user: int):
    fornow = f"📌PIN: {message.text}"
    try:
        sent_message = bot.send_message(user, fornow)
        bot.pin_chat_message(user, sent_message.message_id)
        bot.send_message(message.chat.id, "Xabar muvaffaqiyatli PINda o'rnatildi✅.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ushbu user xatoligi tufayli PINda o'rnatilmadi {user}: {str(e)}")



#unpin from one user
@bot.message_handler(commands=['unpin'])
def unpin_message_for_user(message: types.Message):
    chat_id = message.chat.id

    if int(chat_id) != 6956376313:
        msg = "Siz admin emasligingiz tufayli, bu huquqdan foydalana olmaysiz!🚫"
        bot.send_message(message.chat.id, msg)
        bot.delete_message(chat_id=chat_id, message_id=message.id)
        return
    else:
        bot.send_message(message.chat.id, "PINni olib tashlash kerak bo`lgan user IDsini kiriting: ")
        bot.register_next_step_handler(message, unget_user_id_and_pin_message)


def unget_user_id_and_pin_message(message: types.Message):
    try:
        user_id = int(message.text)
        user = cursor.execute("select user_id from user where id = ?", (user_id,)).fetchone()
        if user:
            bot.unpin_chat_message(user[0])
            bot.send_message(message.chat.id, "Xabar muvaffaqiyatli PINdan olib tashlandi✅.")
        else:
            bot.send_message(message.chat.id, "Mavjud bo`lmagan ID kiritdingiz!")
    except ValueError:
        bot.send_message(message.chat.id, "ID faqat raqamdan iborat bo'lishi kerak!")




@bot.message_handler(commands=['sms'])
def sms_sender(message: types.Message):
    bot.send_message(message.chat.id, "Matnni kiriting: ", reply_to_message_id=message.message_id)
    bot.register_next_step_handler(message, send_message_to_admin)


def send_message_to_admin(message: types.Message):
    user = cursor.execute("select id, first_name, username from user where user_id = ?", (message.from_user.id, )).fetchone()
    user_message = f"ID: {int(user[0])}\nNick: {user[1]}\nUsername: @{user[2]}\n\n===message===\n{message.text}"

    admin_id = 6956376313


    # Forward the user's message to the admin
    # bot.forward_message(admin_id, message.chat.id, message.message_id)
    bot.send_message(admin_id, user_message)
    bot.send_message(message.chat.id, "Xabaringiz muvaffaqiyatli yuborildi✅. Iltimos, admin javobini kuting...", reply_to_message_id=message.message_id)





@bot.message_handler(commands=['users'])
def all_users(message: types.Message):
    x = 6956376313
    chat_id = message.chat.id
    userlar=''

    if int(chat_id) != int(x):
        msg = "Sizda adminlik huquqi yo'q!"
        bot.send_message(message.chat.id, msg)
        bot.delete_message(chat_id=chat_id, message_id=message.id)
        return
    else:
        all_users = cursor.execute("""
                SELECT id, first_name, username FROM user
                """).fetchall()

        # keyboard = types.InlineKeyboardMarkup()
        count=0
        userlar += f"ID   |   NAME   |   USERNAME"
        for user_id, first_name, username in all_users:
            count+=1
            if username:
                # button = types.InlineKeyboardButton(text=f"[{user_id}] {first_name} ✅",
                #                                     url=f"https://t.me/{username}")
                userlar += f"\n{count}   |   {first_name}   |    @{username} ✅"
            else:
                # button = types.InlineKeyboardButton(text=f"[{user_id}] {first_name} 🚫",
                #                                     url=f"https://t.me/{username}")
                userlar += f"\n{count}   |   {first_name}   |    empty ❌ "

            # Create an inline button with the user's name as text

            # Add the button to the keyboard
            # keyboard.add(button)

        # bot.send_message(chat_id=chat_id, text=f"Ayni vaqtdagi foydalanuvchilar: {count} ta", reply_markup=keyboard)
        userlar += f"\n\n===============================\nAyni vaqtdagi foydalanuvchilar: {count} ta"

        max_length = 4096
        userlar += f"\n\nMatnning uzunligi ==> {len(userlar)}"
        if len(userlar) > max_length:
        # Split the message into smaller chunks and send each chunk separately
            for i in range(0, len(userlar), max_length):
                chunk = userlar[i:i + max_length]
                bot.send_message(chat_id, text=chunk)
        else:
            bot.send_message(chat_id, text=userlar)
        # bot.send_message(chat_id=chat_id, text=userlar)


# def all_users(message: types.Message):
#     x = os.getenv('admin')
#     chat_id = message.chat.id
#
#     if int(chat_id) != int(x):
#         msg = "ukam sen admin emassan!"
#         bot.send_message(message.chat.id, msg)
#         bot.delete_message(chat_id=chat_id, message_id=message.id)
#         return
#     else:
#         all_users = cursor.execute("""
#                 select id, first_name, username from user
#                 """).fetchall()
#         # print(all_users)
#         text = ''
#         text += 'ID |  NAME  |  USERNAME\n'
#         for a, b, c in all_users:
#             if c:
#                 profile_link = f"https://t.me/{c}"
#                 text += f"{a}  |  {b}  |  [{c}]({profile_link})\n"
#             else:
#                 text += f"{a}  |  {b}  |  🚫\n"
#
#         bot.send_message(chat_id=chat_id, text=text)










@bot.message_handler(commands=['stats'])
def admin_management(message: types.Message):
    x = 6956376313
    chat_id = message.chat.id

    if int(chat_id) != int(x):
        msg = "ukam sen admin emassan!"
        bot.send_message(message.chat.id, msg)
        bot.delete_message(chat_id=chat_id, message_id=message.id)
        return
    else:
        users_messages = dict()

        users = cursor.execute("""
        select id, first_name from user
        """).fetchall()
        # print(users)

        messages = cursor.execute("""
        select content, translated_content, user_id from message
        """).fetchall()
        # print(messages)

        for user_id, first_name in users:
            k = list()
            for message in messages:
                if int(message[2]) == int(user_id):
                    k.append({message[0] : message[1]})
            users_messages[first_name] = k
        print(users_messages)

        text = ""
        for user, content in users_messages.items():
            text+=f"{user}"
            for k in content:
                text+=f"\n{k}"
            text+="\n====================\n"

        create_json_file(f'statistics', users_messages)
        with open('json_folder/statistics.txt', mode='rb') as json_file:
            content = json_file.read()

        # bot.send_message(chat_id=chat_id, text=text)

        def send_message(chat_id, message):
            # Check if the message length exceeds the maximum allowed length
            max_length = 4096
            message += f"\n\nMatnning uzunligi ==> {len(message)}"
            if len(message) > max_length:
                # Split the message into smaller chunks and send each chunk separately
                for i in range(0, len(message), max_length):
                    chunk = message[i:i + max_length]
                    bot.send_message(chat_id, chunk)
            else:
                bot.send_message(chat_id, message)
        send_message(chat_id, text)



        bot.send_document(chat_id, content, visible_file_name="statistics")







@bot.message_handler(commands = ['start'])
def start_something(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    text = f"Assalomu alaykum, {first_name}\nO'zgartirmoqchi bo'lgan matningizni kiriting!"
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_to_message_id=message.message_id
    )
    url_video = open('/home/FirePlay/first_bot/hello.mp4', mode='rb')
    bot.send_video(message.chat.id, url_video, width=1980, height=1020, caption="📹Botning barcha imkoniyatlarini bilish uchun videoni ko'ring...")
    url_video.close()
    user = cursor.execute("SELECT id FROM user WHERE user_id = ?", (chat_id,)).fetchone()
    if not user:
        cursor.execute(
            """
            INSERT INTO user (user_id, first_name, username) VALUES(?, ?, ?);
            """, (chat_id, first_name, username)
        )
        db.commit()

# @bot.message_handler()
# def reply(message: types.Message):
#     url_video = open('/home/fireplay/Desktop/RECORDS/chochqa.mp4', mode='rb')
#     bot.send_video(message.chat.id, url_video, reply_to_message_id=int(message.id), caption='Barakalla 😁')
#     url_video.close()

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    text = message.caption
    print(text, type(text))
    isLatin_orCirill = True
    import re

    def contains_cyrillic(text):
        return bool(re.search('[\u0400-\u04FF]', text))

    if text.isascii():
        z = to_cyrillic(text)
    else:
        if not text.isascii():
            if contains_cyrillic(text):
                z = to_latin(text)
            else:
                isLatin_orCirill = False
        else:
            isLatin_orCirill = False
    if not isLatin_orCirill:
        bot.send_message(chat_id, text="Siz kiritgan matn, UTF-8 standartiga mos kelmaydi!",
                         reply_to_message_id=message.id)
    else:
        user_id = int(cursor.execute("select id from user where user_id = ?", (chat_id,)).fetchone()[0])
        # <>
        photo_file_id = message.photo[-1].file_id  # get the largest photo
        print(photo_file_id)

        # You can also download the photo if needed
        photo_info = bot.get_file(photo_file_id)
        photo_path = photo_info.file_path
        downloaded_photo = bot.download_file(photo_path)
        # Then you can save/process the downloaded_photo as needed
        with open("downloaded_photo.jpg", "wb") as file:
            file.write(downloaded_photo)

        # Download the photo to your local machine
        photo_url = f"https://api.telegram.org/file/bot{bot.token}/{photo_path}"
        # downloaded_photo = bot.download_file(photo_url, 'downloaded_photo.jpg')
        bot.send_photo(chat_id, open("downloaded_photo.jpg", "rb"), caption=z, reply_to_message_id=message.message_id)
        cursor.execute("""
                    INSERT INTO message (message_id, content, translated_content, user_id) VALUES (?, ?, ?, ?)
                    """, (message.message_id, text, z, user_id))
        db.commit()


@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    text = message.caption
    print(text, type(text))
    isLatin_orCirill = True
    import re

    def contains_cyrillic(text):
        return bool(re.search('[\u0400-\u04FF]', text))

    if text.isascii():
        z = to_cyrillic(text)
    else:
        if not text.isascii():
            if contains_cyrillic(text):
                z = to_latin(text)
            else:
                isLatin_orCirill = False
        else:
            isLatin_orCirill = False
    if not isLatin_orCirill:
        bot.send_message(chat_id, text="Siz kiritgan matn, UTF-8 standartiga mos kelmaydi!",
                         reply_to_message_id=message.id)
    else:
        user_id = int(cursor.execute("select id from user where user_id = ?", (chat_id,)).fetchone()[0])

        # Get the file ID of the video
        video_file_id = message.video.file_id

        # You can also download the video if needed
        video_info = bot.get_file(video_file_id)
        video_path = video_info.file_path
        downloaded_video = bot.download_file(video_path)

        # Save the downloaded video locally
        with open("downloaded_video.mp4", "wb") as file:
            file.write(downloaded_video)

        # Send the video along with its caption translated
        bot.send_video(chat_id, open("downloaded_video.mp4", "rb"), caption=z, reply_to_message_id=message.message_id)

        # Insert message into the database
        cursor.execute("""
                    INSERT INTO message (message_id, content, translated_content, user_id) VALUES (?, ?, ?, ?)
                    """, (message.message_id, text, z, user_id))
        db.commit()


@bot.message_handler()
def nima(message: types.Message):
    chat_id = message.chat.id
    # print(message.id)
    print(chat_id)

    user_id = int(cursor.execute("select id from user where user_id = ?", (chat_id,)).fetchone()[0])
    print(user_id)
    message_id = message.message_id
    text = message.text
    isLatin_orCirill=True
    import re

    def contains_cyrillic(text):
        return bool(re.search('[\u0400-\u04FF]', text))

    if message.text.isascii():
        z = to_cyrillic(message.text)
    else:
        if not message.text.isascii():
            if contains_cyrillic(text):
                z = to_latin(text)
            else:
                isLatin_orCirill = False
        else:
            isLatin_orCirill=False
    if not isLatin_orCirill:
        bot.send_message(chat_id, text="Siz kiritgan matn, UTF-8 standartiga mos kelmaydi!\nFaqat text kiriting!", reply_to_message_id=message.id)
    else:
        print("> > > > >>")
        bot.send_message(chat_id, z, reply_to_message_id=message.id)
        cursor.execute("""
            INSERT INTO message (message_id, content, translated_content, user_id) VALUES (?, ?, ?, ?)
            """, (message_id, text, z, user_id))
        db.commit()





while True:
    try:
        print("Starting...")
        bot.polling(non_stop=True, skip_pending=True)
    except Exception as e:
        print(e)
        time.sleep(5)
        print("Bot is worked")
