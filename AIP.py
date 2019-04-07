# -*- coding: utf-8 -*-
#!/usr/bin/python

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from emoji import emojize
import sqlite3
import os

PORT = int(os.environ.get('PORT', '5000'))

TOKEN = '833279811:AAHLL0-Y3R5VHLXtbNw3OOFFdtgXvzTBQWE'
USER = {}


def database(sql):
    db = sqlite3.connect("AIP.db")
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result

def start(bot, update):
    global USER

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

    bot.send_message(text=msg, chat_id=112137855)
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
    elif len(USER[user]) == 1:
        msg, reply_markup = part_button(bot, update, user)
        bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode=ParseMode.MARKDOWN,
                          reply_markup=reply_markup)
        
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
                          caption=caption)
        msg = "The file *%s* has been send. \n\nPress the button below to go back to the menu." %name
        bot.send_message(text="the filed has been sent",
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

updater.dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(CommandHandler("start", start))

#updater.start_polling()
updater.start_webhook(listen="0.0.0.0",
                       port=PORT,
                       url_path=TOKEN)
updater.bot.setWebhook("https://iranaip.herokuapp.com/" + TOKEN)
updater.idle()
