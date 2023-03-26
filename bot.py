import os
import telebot
from dotenv import dotenv_values
import requests
from prettytable import PrettyTable


BOT_TOKEN = dotenv_values(".env")["BOT_TOKEN"]

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Attendd for KLE Tech\n\nHowdy, how are you doing?\nTo get your attendence and CIE marks, \n\nType your USN followed by space and then Date of Birth (DD-MM-YYYY):\n\nExample:\n01fe20bcs500 23-01-2002",
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
        response += f"""\nCourse Code: {i["course_code"]}\nCourse Name: {i["course_name"]}\nAttendance: {i["course_attendance"]}\nCIE: {i["cie_marks"]}\n"""
    response += "\n\nTo get updated details, \n_Type your USN followed by space and then Date of Birth (DD-MM-YYYY):\n\nExample:\n01fe20bcs500 23-01-2002"
    bot.reply_to(message, str(response))


bot.infinity_polling()
