from subprocess import check_output
import telebot
import datetime
import pytz
import time

bot = telebot.TeleBot("")
user_id = 0123456789

@bot.message_handler(commands=['start'])
def greet(message):
  user_first_name = str(message.chat.first_name) 
  bot.reply_to(message, f"Hey! {user_first_name} \nWelcome To The Power Schedule bot!\nAt the bottom you will find a button.\nWhen you press it I will give you the info. \nTry it out!")
  user_id=message.from_user.id
  print(user_id)
  button_schedule = telebot.types.KeyboardButton('Power Schedule')
  keyboard = telebot.types.ReplyKeyboardMarkup()
  keyboard.add(button_schedule)
  bot.send_message(user_id, text='Press the button', reply_markup=keyboard)


button_schedule = telebot.types.KeyboardButton('Power Schedule')
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.add(button_schedule)
bot.send_message(user_id, text='Press the button', reply_markup=keyboard)
#@bot.message_handler(func=lambda message: message.text == "Power Schedule")
#@bot.callback_query_handler(func=lambda call: True)
#def callback_query(call):
@bot.message_handler(content_types=["text"])
def main(message):
    if message.text == "Power Schedule":
      try:
        ua = pytz.timezone('Europe/Kiev')
        now = datetime.datetime.now(ua)

        schedule = [{"grey": [0,7,8,9,16,17,18], "white": [1,2,10,11,19,20], "black": [3,4,5,6,12,13,14,15,21,22,23]},
                    {"grey": [1,2,3,10,11,12,19,20,21], "white": [4,5,13,14,22,23], "black": [0,6,7,8,9,15,16,17,18]},
                    {"grey": [4,5,6,13,14,15,22,23], "white": [7,8,16,17], "black": [0,1,2,3,9,10,11,12,18,19,20,21]},
                    {"grey": [0,7,8,9,16,17,18], "white": [1,2,10,11,19,20], "black": [3,4,5,6,12,13,14,15,21,22,23]},
                    {"grey": [1,2,3,10,11,12,19,20,21], "white": [4,5,13,14,22,23], "black": [0,6,7,8,9,15,16,17,18]},
                    {"grey": [4,5,6,13,14,15,22,23], "white": [7,8,16,17], "black": [0,1,2,3,9,10,11,12,18,19,20,21]},
                    {"grey": [0,7,8,9,16,17,18], "white": [1,2,10,11,19,20], "black": [3,4,5,6,12,13,14,15,21,22,23]}]

        weekday = now.weekday()
        offset = 0

        now_area = ""
        next1_area = ""
        next1_hour = 25
        next2_area = ""
        next2_hour = 0

        next1 = int(now.hour)

        key_list = list(schedule[now.weekday()].keys())
        val_list = list(schedule[now.weekday()].values())

        grand_message = ""

        for area in key_list:
            if int(now.hour) in schedule[now.weekday()][area]:
                now_area = area
                key_list.remove(area)

        for i in range(4):
            if next1 == 23:
                if weekday == 6:
                    weekday = 0
                else: 
                    weekday +=1
                offset = 1
                next1 = 0
            else:
                next1+=1
            for area in key_list:
                if next1 in schedule[weekday][area]:
                    if next1_area == "":
                        next1_date_str = "" + str(now.year) + "," + str(now.month) + "," + str(now.day) + ":" + str(next1) + "-00" + ",+0300"
                        next1_date = datetime.datetime.strptime(next1_date_str, "%Y,%m,%d:%H-%M,%z")
                        if offset == 1:
                            next1_date += datetime.timedelta(days=1)
                        diff = next1_date - now
                        grand_message += "Now it is " + now_area.upper() + " zone, and it will be for another " + str(diff).split(".")[0] + ".\n"
                        grand_message += "Then it will be " + area.upper() + " zone, at " + str(next1) + ":00\n"
                        next1_area = area
                        next1_hour = next1
                        key_list.remove(area)
                    else:
                        next2_date_str = "" + str(now.year) + "," + str(now.month) + "," + str(now.day) + ":" + str(next1) + "-00" + ",+0300"
                        next2_date = datetime.datetime.strptime(next2_date_str, "%Y,%m,%d:%H-%M,%z")
                        if offset == 1:
                            next2_date += datetime.timedelta(days=1)
                        diff = next2_date - now
                        grand_message += "Next " + area.upper() + " will be in " + str(diff).split(".")[0] + ",at " + str(next1) + ":00."
                        next2_area = area
                        next2_hour = next1
                        key_list.remove(area)
                    break

        if len(key_list) > 0:
            for i in range(4):
                if next1 == 23:
                    if weekday == 6:
                        weekday = 0
                    else: 
                        weekday +=1
                    offset = 1
                    next1 = 0
                else:
                    next1+=1
                for area in key_list:
                    if next1 in schedule[weekday][area]: 
                        next2_date_str = "" + str(now.year) + "," + str(now.month) + "," + str(now.day) + ":" + str(next1) + "-00" + ",+0300"
                        next2_date = datetime.datetime.strptime(next2_date_str, "%Y,%m,%d:%H-%M,%z")
                        if offset == 1:
                            next2_date += datetime.timedelta(days=1)
                        diff = next2_date - now
                        grand_message += "Next " + area.upper() + " will be in " + str(diff).split(".")[0] + ",at " + str(next1) + ":00."
                        next2_area = area
                        next2_hour = next1
                        key_list.remove(area) 
        bot.send_message(message.chat.id, grand_message)
      except Exception as error:
          print("Something went wrong: ",error)
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)
