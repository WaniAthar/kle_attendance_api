import os
import telebot
from dotenv import dotenv_values
import requests

BOT_TOKEN = dotenv_values(".env")["BOT_TOKEN"]

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Attendd for KLE Tech\nHowdy, how are you doing?\nTo get your attendance and CIE marks, \n\n_Type your USN followed by space and then Date of Birth (DD-MM-YYYY):_\n\n_Example:_\n_01fe20bcs500 23-01-2002_",
    )


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print(message.text)
    q = message.text.split(" ")
    usn = q[0].strip().upper()
    d = q[1].split("-")
    dob = d[2] + "-" + d[1] + "-" + d[0]
    reply = requests.get(
        f"https://helloapi-ozaf.onrender.com/attendance/username={usn}_and_password={dob}"
    ).json()

    # Specify the Column Names while initializing the Table
    response = "Here is your data: \n"
    # Add rows
    for i in reply:
        response += f"""\n**Course Code**: {i["course_code"]}\n**Course Name**: {i["course_name"]}\n**Attendance**: {i["course_attendance"]}\n**CIE**: {i["cie_marks"]}\n"""
    response += "\n\n_To get updated details,_ \n_Type your USN followed by space and then Date of Birth (DD-MM-YYYY):_\n\n_Example:_\n_01fe20bcs500 23-01-2002_"
    bot.reply_to(message, str(response))


bot.infinity_polling()
