# -*- coding: utf-8 -*-
#!/usr/bin/python

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from emoji import emojize
import sqlite3
import os
import random

PORT = int(os.environ.get('PORT', '5000'))

#833279811:AAHLL0-Y3R5VHLXtbNw3OOFFdtgXvzTBQWE
TOKEN = '833279811:AAHLL0-Y3R5VHLXtbNw3OOFFdtgXvzTBQWE'
USER = {}
SEARCH = {}
ADS = {1:"http://s9.picofile.com/file/8357252342/test.jpg---%s درسگفتارهای هوانوردی، آموزش تصویری بوکلت‌های سازمان هواپیمایی کشوری، اگهی‌های استخدام و هر آنچه شما از هوانوردی به آن نیاز دارید. %s \n\n%s عضویت از طریق ID زیر:\n%s @AviationCourse" % (emojize(":blue_book:", use_aliases=True),
                               emojize(":closed_book:", use_aliases=True),
                               emojize(":white_check_mark:", use_aliases=True),
                               emojize(":id:", use_aliases=True)),
       2: "http://s8.picofile.com/file/8357694600/met.jpg---%s #هواشناسي\n\n%s اطلاع رسانی اخبار، اطلاعیه ها، اخطاریه ها و پیش بینی های هواشناسی به عموم مردم زیر نظر سازمان هواشناسی\n\n%s https://t.me/Irimo_warning" % (emojize(":ocean:", use_aliases=True),
                                                                                                                                                                                                                           emojize(":mega:", use_aliases=True),
                                                                                                                                                                                                                           emojize(":globe_with_meridians:", use_aliases=True)}


def database(sql):
    db = sqlite3.connect("AIP.db")
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result

def start(bot, update):
    global USER
    global ADS

    capt = "%s درسگفتارهای هوانوردی، آموزش تصویری بوکلت‌های سازمان هواپیمایی کشوری، اگهی‌های استخدام و هر آنچه شما از هوانوردی به آن نیاز دارید. %s \n\n%s عضویت از طریق ID زیر:\n%s @AviationCourse" % (emojize(":blue_book:", use_aliases=True),
                               emojize(":closed_book:", use_aliases=True),
                               emojize(":white_check_mark:", use_aliases=True),
                               emojize(":id:", use_aliases=True))
    user = update.effective_user.id
    msg = "The user with the following information has just started the AIP Bot:\n"
    try:
        first_name = update.effective_user.first_name
        msg += "\nFirstname : %s" % str(first_name)
    except:
        pass
    try:
        last_name = update.effective_user.last_name
        msg += "\nLastname : %s" % str(last_name)
    except:
        pass
    try:
        chat_id = update.effective_user.id
        msg += "\nChat ID : %s" % str(chat_id)
    except:
        pass
    try:
        username = update.effective_user.username
        msg += "\nUsername : @%s" % str(username)
    except:
        pass
    ads = random.randint(1, 2)
    link = ADS[ads].split("---")[0]
    capt = ADS[ads].split("---")[1]  
    bot.send_message(text=msg, chat_id=112137855)
    bot.send_photo(chat_id = user,
                   photo = link,
                   caption = capt)
    USER[user] = []
    SEARCH[user] = []
    aip = ['GEN', 'ENR', 'AD']
    keyboard = []
    msg = "*List of AIP parts:*\n\n"

    for i in range(len(aip)):
        msg += "\t\t" + str(i + 1) + ". " + aip[i] + "\n"
        row = []
        row.append(InlineKeyboardButton(str(aip[i]), callback_data=aip[i]))
        keyboard.append(row)

    msg += "\n_Please select your desired AIP part:_"
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


def aip(bot, update):
    global USER

    user = update.effective_user.id
    USER[user] = []
    aip = ['GEN', 'ENR', 'AD']
    keyboard = []
    msg = "*List of AIP parts:*\n\n"

    for i in range(len(aip)):
        msg += "\t\t" + str(i + 1) + ". " + aip[i] + "\n"
        row = []
        row.append(InlineKeyboardButton(str(aip[i]), callback_data=aip[i]))
        keyboard.append(row)

    msg += "\n_Please select your desired AIP part:_"
    reply_markup = InlineKeyboardMarkup(keyboard)
    return msg, reply_markup

def howto(bot, update):
    global USER
    msg = '''%s موارد و نحوه استفاده از بات:

1. برای دسترسی به AIP از دستور /start استفاده کنید.

2. برای جست و جو کردن چارت، SID، STAR و IAC مورد نظر خود، کافی است کلید مورد نظر خود را تایپ کنید. به عنوان مثال:

dehnamak 3a
parot
oiii ils
oitt circling ndb''' % emojize(":loudspeaker:", use_aliases=True)
    user = update.effective_user.id
    bot.send_message(chat_id=user,
                     text=msg)

def search(bot, update):
    global USER
    global SEARCH
    user = update.effective_user.id
    text = update.message.text
    text = text.split(' ')
    keyboard = []
    row = []
    counter = 1
    USER[user] = []
    SEARCH[user] = []
    airport = ''
    msg = emojize(":mag_right:", use_aliases=True) + ' Search result:\n\n'
    for re in text:
        if 'oi' in re.lower():
            result = database("SELECT file_description FROM 'AD2' WHERE part_name='%s';" % re.upper())
            text.remove(re)
            airport = re
        else:
            result = database("SELECT file_description FROM 'AD2';")
    for item in result:
        for re in text:
            if re.lower() in item[0].lower():
                continue
            else:
                break
        else:
            if airport == '':
                aerodrome = database("SELECT part_name FROM 'AD2' WHERE file_description='%s';" % item[0])
                aerodrome = aerodrome[0][0]
            else:
                aerodrome = airport.upper()
            msg += str(counter) + ". " + aerodrome + " - " + item[0] + "\n"
            row.append(InlineKeyboardButton(str(counter), callback_data=counter))
            SEARCH[user].append(aerodrome + " + " + item[0])
            if len(row) % 5 == 0:
                keyboard.append(row)
                row = []
            counter += 1
    keyboard.append(row)
    msg += '\n\n_Select the number of your search result:_'
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id = user,
                     text = msg,
                     parse_mode=ParseMode.MARKDOWN,
                     reply_markup=reply_markup)
    
    
def button(bot, update):
    global USER
    user = update.effective_user.id
    query = update.callback_query
    option_name = query.data
    USER[user].append(option_name)


    #This part deals with the users back action
    if option_name == "back":
        USER[user] = USER[user][:-2]

    if len(USER[user]) == 0:
        msg, reply_markup = aip(bot, update)
        bot.edit_message_text(text=msg,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=reply_markup)

    #This part means that the user has selected one of the three parts of the AIP (GEN, ENR, AD)
    elif len(USER[user]) == 1 and len(SEARCH[user]) == 0:
        msg, reply_markup = part_button(bot, update, user)
        bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=ParseMode.MARKDOWN,
                          reply_markup=reply_markup)
    elif len(USER[user]) == 1 and len(SEARCH[user]) > 0:
        bot.delete_message(chat_id=query.message.chat_id,
                           message_id=query.message.message_id)
        
        result = database("SELECT * FROM 'AD2' WHERE part_name='%s' AND file_description='%s';" % (SEARCH[user][int(USER[user][0]) - 1].split(" + ")[0], SEARCH[user][int(USER[user][0]) - 1].split(" + ")[1]))
        link    = result[0][4]
        name    = result[0][2]
        caption = result[0][3]
        bot.send_document(chat_id=user,
                        document=link,
                          filename=name,
                          caption= emojize(":page_facing_up:", use_aliases=True) + " " + caption + "\n\n%s @IranAIPBot" % emojize(":id:", use_aliases=True))
    elif USER[user][-1] == 'AD 2':
        msg, reply_markup = aerodromes_button(bot, update, user)
        bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=ParseMode.MARKDOWN,
                          reply_markup=reply_markup)
    #This part means that the user has selected the subpart of one the parts excluding AD 2
    elif len(USER[user]) == 2 or (USER[user][1] == 'AD 2' and len(USER[user]) == 3):
        msg, reply_markup = subPart_button(bot, update, user)
        bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=ParseMode.MARKDOWN,
                          reply_markup=reply_markup)

    elif len(USER[user]) >= 3:
        link, name, caption, reply_markup = file(bot, update, user)
        bot.delete_message(chat_id=query.message.chat_id,
                           message_id=query.message.message_id)
        
        bot.send_document(chat_id=query.message.chat_id,
                        document=link,
                          filename=name,
                          caption= emojize(":page_facing_up:", use_aliases=True) + " " + caption + "\n\n%s @IranAIPBot" % emojize(":id:", use_aliases=True))
        msg = "%s The file *%s* has been sent. \n\nPress the button below to go back to the menu." % (emojize(":white_check_mark:", use_aliases=True),
                                                                                                      name)
        bot.send_message(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=ParseMode.MARKDOWN,
                          reply_markup=reply_markup)

def part_button(bot, update, user):
    result = database("SELECT * FROM '%s';" % USER[user][0])
    keyboard = []
    msg = emojize(":books:", use_aliases=True) + " *Selected AIP part: * _%s_\n\n" % USER[user][0]
    list_counter = 1
    row = []
    for i in range(len(result)):
        if str(result[i][0]) in msg:
            pass
        else:
            msg += "\t\t" + str(list_counter) + ".\t" + "*" + str(result[i][0])+ "*" + " (_ " + str(result[i][1]) + " _) " +  "\n"
            row.append(InlineKeyboardButton(str(result[i][0]), callback_data=result[i][0]))
            if len(row) % 4 == 0:
                keyboard.append(row)
                row = []
            list_counter += 1
    else:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Go Back to AIP", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return msg, reply_markup

def aerodromes_button(bot, update, user):
    result = database("SELECT * FROM 'AD2';")
    keyboard = []
    msg = """%s *Selected AIP part:* _%s_
%s *Selected section:* _%s_
\n_Please select your desired aerodrome_:\n\n""" % (emojize(":books:", use_aliases=True),
                                    USER[user][0],
                                    emojize(":closed_book:", use_aliases=True),
                                    USER[user][1])
    list_counter = 1
    row = []
    for i in range(len(result)):
        if str(result[i][0]) in msg:
            pass
        else:
            msg += "\t\t" + str(list_counter) + ".\t" + "*" + str(result[i][0])+ "*" + " (_ " + str(result[i][1]) + " _) " +  "\n"
            row.append(InlineKeyboardButton(str(result[i][0]), callback_data=result[i][0]))
            if len(row) % 5 == 0:
                keyboard.append(row)
                row = []
            list_counter += 1
    else:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Go Back to AD", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return msg, reply_markup    

def subPart_button(bot, update, user):
    if USER[user][1] == 'AD 2':
        result = database("SELECT * FROM 'AD2' WHERE part_name='%s';" %  USER[user][2])
        msg = """%s *Selected AIP part:* _%s_
%s *Selected section:* _%s_
%s *Selected aerodrome:* _%s_
\n_Please select your desired file_:\n\n""" % (emojize(":books:", use_aliases=True),
                                    USER[user][0],
                                    emojize(":closed_book:", use_aliases=True),
                                    USER[user][1],
                                    emojize(":airplane:", use_aliases=True),
                                    USER[user][2])
    else:
        result = database("SELECT * FROM '%s' WHERE part_name='%s';" % (USER[user][0], USER[user][1]))
        msg = """%s *Selected AIP part:* _%s_
%s *Selected section:* _%s_
\n_Please select your desired file_:\n\n""" % (emojize(":books:", use_aliases=True),
                                    USER[user][0],
                                    emojize(":closed_book:", use_aliases=True),
                                    USER[user][1])
    keyboard = []
    row = []
    for i in range(len(result)):
        msg += text_editor(str(result[i][2]), result[i][0]) + "\t\t" + str(i + 1) + ".\t" + "*" + str(result[i][2]) + "*" + " (_ " + str(result[i][3]) + " _) " + "\n"
        row.append(InlineKeyboardButton(str(result[i][2]), callback_data=result[i][2]))
        if len(row) % 4 == 0:
                keyboard.append(row)
                row = []
    else:
        keyboard.append(row)
    if USER[user][1] == 'AD 2':
        keyboard.append([InlineKeyboardButton("Go Back to AD 2", callback_data="back")])
    else:
        keyboard.append([InlineKeyboardButton("Go Back to %s" % USER[user][0], callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return msg, reply_markup


def file(bot, update, user):
    if USER[user][1] == "AD 2":
        result = database("SELECT * FROM 'AD2' WHERE part_name='%s' AND file_name='%s';" % ( USER[user][2], USER[user][3]))
    else:
        result = database("SELECT * FROM '%s' WHERE part_name='%s' AND file_name='%s';" % (USER[user][0], USER[user][1], USER[user][2]))
    link    = result[0][4]
    name    = result[0][2]
    caption = result[0][3]
    keyboard = []
    if USER[user][1] == "AD 2":
        keyboard.append([InlineKeyboardButton("Go Back to %s" % USER[user][2], callback_data="back")])
    else:
        keyboard.append([InlineKeyboardButton("Go Back to %s" % USER[user][1], callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return link, name, caption, reply_markup

def text_editor(text, part):
    if "OI" in text:
        return emojize(":airplane:", use_aliases=True)
    elif "ADC" in text:
        return emojize(":world_map:", use_aliases=True)
    elif "SID" in text:
        return emojize(":airplane_departure:", use_aliases=True)
    elif "IAC" in text:
        return emojize(":airplane_arriving:", use_aliases=True)
    elif "STAR" in text:
        return emojize(":small_airplane:", use_aliases=True)
    elif "AOC" in text:
        return emojize(":building_construction:", use_aliases=True)
    elif "PDC" in text:
        return emojize(":parking:", use_aliases=True)
    elif "VFR" in text:
        return emojize(":helicopter:", use_aliases=True)
    elif "ARC" in text:
        return emojize(":mountain:", use_aliases=True)
    elif "ASMAC" or "PATC" in text:
        return emojize(":satellite:", use_aliases=True)
    else:
        return ""
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(MessageHandler(Filters.text, search))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", howto))

#updater.start_polling()
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                     url_path=TOKEN)
updater.bot.setWebhook("https://iranaip.herokuapp.com/" + TOKEN)
updater.idle()
