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
ADS = {1 : "http://s9.picofile.com/file/8357252342/test.jpg---%s درسگفتارهای هوانوردی، آموزش تصویری بوکلت‌های سازمان هواپیمایی کشوری، اگهی‌های استخدام و هر آنچه شما از هوانوردی به آن نیاز دارید. %s \n\n%s عضویت از طریق ID زیر:\n%s @AviationCourse" % (emojize(":blue_book:", use_aliases=True),
                               emojize(":closed_book:", use_aliases=True),
                               emojize(":white_check_mark:", use_aliases=True),
                               emojize(":id:", use_aliases=True)),
       2 : '''http://s8.picofile.com/file/8358542034/aviatraining.jpg---[اویاترینینگ](http://aviatraining.ir/) بزرگترین و معتبرترین مرجع آموزش هوانوردی است که با تلاش مستمر یک تیم عظیم علمی و تخصصی متشکل از خلبانان، مهندسین مراقبت پرواز، تکنسین های تعمیر و نگهداری هواپیما و... سعی بر آموزش منسجم منابع رسمی و معتبر این صنعت به تمامی علاقه مندان دارد.

هم اکنون به جمع ما بپیوندید

[وب سایت رسمی ما](http://aviatraining.ir/) | [کانال تلگرامی ما](https://t.me/aviatraining) | [صفحه ما در اینستاگرام](https://instagram.com/aviatraining.ir)'''
       }

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
    ads = random.randint(1, 10)
    if ads >= 3:
        ads = 2
    else:
        ads = 1
    link = ADS[ads].split("---")[0]
    capt = ADS[ads].split("---")[1]
    bot.send_message(text=msg, chat_id=112137855)
    bot.send_photo(chat_id = user,
                   photo = link,
                   caption = capt,
                   parse_mode=ParseMode.MARKDOWN)
    USER[user] = []
    SEARCH[user] = []
    aip = ['GEN', 'ENR', 'AD']
    keyboard = []
    msg = "*List of AIP parts:*\n\n"
    row = []
    for i in range(len(aip)):
        msg += "\t\t" + str(i + 1) + ". " + aip[i] + "\n"
        row.append(InlineKeyboardButton(str(aip[i]), callback_data=aip[i]))
    keyboard.append(row)
    row = []
    row.append(InlineKeyboardButton('AIC', callback_data='AIC'))
    row.append(InlineKeyboardButton('SUP', callback_data='SUP'))
    keyboard.append(row)
    #row = []
    #row.append(InlineKeyboardButton('AIRAC 2/19', callback_data='AIRAC'))
    #keyboard.append(row)
    msg += "\n*Additional Parts:*\n\n\t\t1. AIC\n\t\t2. SUP\n"

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

    row = []
    for i in range(len(aip)):
        msg += "\t\t" + str(i + 1) + ". " + aip[i] + "\n"
        row.append(InlineKeyboardButton(str(aip[i]), callback_data=aip[i]))
    keyboard.append(row)
    row = []
    row.append(InlineKeyboardButton('AIC', callback_data='AIC'))
    row.append(InlineKeyboardButton('SUP', callback_data='SUP'))
    keyboard.append(row)
    #row = []
    #row.append(InlineKeyboardButton('AIRAC 2-19', callback_data='AIRAC'))
    #keyboard.append(row)
    msg += "\n*Additional Parts:*\n\n\t\t1. AIC\n\t\t2. SUP\n"

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
    f = open("Routes.txt", "r")
    routes = f.readlines()
    f.close()
    msg = emojize(":mag_right:", use_aliases=True) + ' Search result:\n\n'
    if len(text) == 1:
        for route in routes:
            if text[0].upper() in route.split(":")[1]:
                msg += emojize(":motorway:", use_aliases=True) + " The Routes which cross through *%s* are:\n" % text[0].upper()
                break
            elif text[0].upper() == route.split(":")[0]:
                msg += emojize(":small_red_triangle:", use_aliases=True) + " The Points which *%s* crosses through are: \n" % text[0].upper()
                break
        for route in routes:
            if text[0].upper() in route.split(":")[1]:
                msg += "\n_" + route.split(":")[0] + "_"
            elif text[0].upper() == route.split(":")[0]:
                msg += "_\n" + route.split(":")[1] + "_"
    msg += "\n\n%s The files that contain your search keyword:\n\n" % emojize(":ledger:", use_aliases=True)
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
        USER[user] = []
        aip = ['GEN', 'ENR', 'AD']
        keyboard = []
        msg = "*List of AIP parts:*\n\n"

        row = []
        for i in range(len(aip)):
            msg += "\t\t" + str(i + 1) + ". " + aip[i] + "\n"
            row.append(InlineKeyboardButton(str(aip[i]), callback_data=aip[i]))
        keyboard.append(row)
        row = []
        row.append(InlineKeyboardButton('AIC', callback_data='AIC'))
        row.append(InlineKeyboardButton('SUP', callback_data='SUP'))
        keyboard.append(row)
        #row = []
        #row.append(InlineKeyboardButton('AIRAC 2-19', callback_data='AIRAC'))
        #keyboard.append(row)
        msg += "\n*Additional Parts:*\n\n\t\t1. AIC\n\t\t2. SUP\n"

        msg += "\n_Please select your desired AIP part:_"
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(text=msg,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=reply_markup)

    #This part means that the user has selected one of the three parts of the AIP (GEN, ENR, AD)
    elif len(USER[user]) == 1 and len(SEARCH[user]) == 0 and USER[user][0] != 'AIRAC':
        msg, reply_markup = part_button(bot, update, user)
        bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=ParseMode.MARKDOWN,
                          reply_markup=reply_markup)
    elif len(USER[user]) == 1 and len(SEARCH[user]) == 0 and USER[user][0] == 'AIRAC':
        aip = ['GEN', 'ENR', 'AD']
        keyboard = []
        msg = "*List of AIRAC AIP parts:*\n\n"

        row = []
        for i in range(len(aip)):
            msg += "\t\t" + str(i + 1) + ". " + aip[i] + "\n"
            row.append(InlineKeyboardButton(str(aip[i]), callback_data=aip[i]))
        keyboard.append(row)
        keyboard.append([InlineKeyboardButton("Go Back to AIP", callback_data="back")])
        msg += "\n_Please select your desired AIRAC AIP part:_"
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=ParseMode.MARKDOWN,
                          reply_markup=reply_markup)
    elif len(USER[user]) == 2 and len(SEARCH[user]) == 0 and USER[user][0] == 'AIRAC':
        msg, reply_markup = airac_part_button(bot, update, user)
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
    elif USER[user][-1] == 'AD 2' and USER[user][0] != 'AIRAC':
        msg, reply_markup = aerodromes_button(bot, update, user)
        bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=ParseMode.MARKDOWN,
                          reply_markup=reply_markup)
    elif USER[user][-1] == 'AD 2' and USER[user][0] == 'AIRAC':
        msg, reply_markup = airac_aerodromes_button(bot, update, user)
        bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=ParseMode.MARKDOWN,
                          reply_markup=reply_markup)
    #This part means that the user has selected the subpart of one the parts excluding AD 2
    elif (len(USER[user]) == 2 and USER[user][0] != 'AIRAC') or (USER[user][1] == 'AD 2' and len(USER[user]) == 3):
        msg, reply_markup = subPart_button(bot, update, user)
        bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=ParseMode.MARKDOWN,
                          reply_markup=reply_markup)
    elif (len(USER[user]) == 3 and USER[user][0] == 'AIRAC') or (USER[user][2] == 'AD 2' and len(USER[user]) == 4):
        msg, reply_markup = airac_subPart_button(bot, update, user)
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
            if str(result[i][1]) != "":
                msg += "\t\t" + str(list_counter) + ".\t" + "*" + str(result[i][0])+ "*" + " (_ " + str(result[i][1]) + " _) " +  "\n"
            else:
                msg += "\t\t" + str(list_counter) + ".\t" + "*" + str(result[i][0])+ "*" +  "\n"
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

def airac_part_button(bot, update, user):
    result = database("SELECT * FROM 'AIRAC_%s';" % USER[user][1])
    keyboard = []
    msg = emojize(":books:", use_aliases=True) + " *Selected AIP part: * _%s_\n\n" % USER[user][1]
    list_counter = 1
    row = []
    for i in range(len(result)):
        if str(result[i][0]) in msg:
            pass
        else:
            if str(result[i][1]) != "":
                msg += "\t\t" + str(list_counter) + ".\t" + "*" + str(result[i][0])+ "*" + " (_ " + str(result[i][1]) + " _) " +  "\n"
            else:
                msg += "\t\t" + str(list_counter) + ".\t" + "*" + str(result[i][0])+ "*" +  "\n"
            row.append(InlineKeyboardButton(str(result[i][0]), callback_data=result[i][0]))
            if len(row) % 4 == 0:
                keyboard.append(row)
                row = []
            list_counter += 1
    else:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Go Back to AIRAC AIP", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return msg, reply_markup

def aerodromes_button(bot, update, user):
    result = sorted(database("SELECT * FROM 'AD2';"))
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

def airac_aerodromes_button(bot, update, user):
    result = sorted(database("SELECT * FROM 'AIRAC_AD2';"))
    keyboard = []
    msg = """%s *Selected AIP part:* _%s_
%s *Selected section:* _%s_
\n_Please select your desired aerodrome_:\n\n""" % (emojize(":books:", use_aliases=True),
                                    USER[user][1],
                                    emojize(":closed_book:", use_aliases=True),
                                    USER[user][2])
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
        result = sorted(database("SELECT * FROM 'AD2' WHERE part_name='%s';" %  USER[user][2]))
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

def airac_subPart_button(bot, update, user):
    if USER[user][2] == 'AD 2':
        result = sorted(database("SELECT * FROM 'AIRAC_AD2' WHERE part_name='%s';" %  USER[user][3]))
        msg = """%s *Selected AIP part:* _%s_
%s *Selected section:* _%s_
%s *Selected aerodrome:* _%s_
\n_Please select your desired file_:\n\n""" % (emojize(":books:", use_aliases=True),
                                    USER[user][1],
                                    emojize(":closed_book:", use_aliases=True),
                                    USER[user][2],
                                    emojize(":airplane:", use_aliases=True),
                                    USER[user][3])
    else:
        result = database("SELECT * FROM 'AIRAC_%s' WHERE part_name='%s';" % (USER[user][1], USER[user][2]))
        msg = """%s *Selected AIP part:* _%s_
%s *Selected section:* _%s_
\n_Please select your desired file_:\n\n""" % (emojize(":books:", use_aliases=True),
                                    USER[user][1],
                                    emojize(":closed_book:", use_aliases=True),
                                    USER[user][2])
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
    if USER[user][2] == 'AD 2':
        keyboard.append([InlineKeyboardButton("Go Back to AD 2", callback_data="back")])
    else:
        keyboard.append([InlineKeyboardButton("Go Back to %s" % USER[user][1], callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return msg, reply_markup

def file(bot, update, user):
    if USER[user][2] == "AD 2":
        result = database("SELECT * FROM 'AIRAC_AD2' WHERE part_name='%s' AND file_name='%s';" % ( USER[user][3], USER[user][4]))
    elif USER[user][1] == "AD 2":
        result = database("SELECT * FROM 'AD2' WHERE part_name='%s' AND file_name='%s';" % ( USER[user][2], USER[user][3]))
    elif USER[user][0] == 'AIRAC':
        result = database("SELECT * FROM 'AIRAC_%s' WHERE part_name='%s' AND file_name='%s';" % (USER[user][1], USER[user][2], USER[user][3]))
    else:
        result = database("SELECT * FROM '%s' WHERE part_name='%s' AND file_name='%s';" % (USER[user][0], USER[user][1], USER[user][2]))
    link    = result[0][4]
    name    = result[0][2]
    caption = result[0][3]
    keyboard = []
    if USER[user][1] == "AD 2":
        keyboard.append([InlineKeyboardButton("Go Back to %s" % USER[user][2], callback_data="back")])
    elif USER[user][2] == "AD 2":
        keyboard.append([InlineKeyboardButton("Go Back to %s" % USER[user][3], callback_data="back")])
    elif USER[user][0] == "AIRAC":
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

def document(bot, update):
    user = update.effective_user.id
    if user == 112137855:
        file = update.effective_message.document.file_id
        name = update.effective_message.document.file_name
        msg = str(name) + '\n' + str(file)
        bot.send_message(chat_id = 112137855,
                         text = msg)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(MessageHandler(Filters.text, search))
dispatcher.add_handler(MessageHandler(Filters.document, document))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", howto))

#updater.start_polling()
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                     url_path=TOKEN)
updater.bot.setWebhook("https://iranaip.herokuapp.com/" + TOKEN)
updater.idle()
