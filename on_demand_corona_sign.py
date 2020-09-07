import argparse
import os
import sys
from datetime import datetime, timezone
from time import strftime, gmtime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import configparser
import logging
import telegram_send

from education_form_filler import EducationWebTopFormFiller
from kasum_form_filler import KasumFormFiller
from nizanim_form_filler import NizanimFormFiller
from really_form_filler import ReallyFormFiller

min_temp = 36
max_temp = 38
max_msg_time = 60 * 1
def is_msg_too_old(msg_datetime):
    return (datetime.now(timezone.utc) - msg_datetime).seconds > max_msg_time

def log_message(message):
    logging.info(message)
    telegram_send.send(conf='master.conf', messages=[message])

def fill_nizanim(update, context):
    log_message(f"{child_first_name} - recieved message " \
        f"from: {update.message.from_user['first_name']} {update.message.from_user['last_name']} " \
        f"at time: {str(update.message.date)} with: {update.message.text}")
    if is_msg_too_old(update.message.date):
        logging.info(
            f"Message too old. Do nothing")
        return
    if update.message.text.lower() == 'fill':
        log_message(f"{child_first_name} - Filling a form for {current_config['child_first_name']}")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"OK, Filling a form for {current_config['child_first_name']} :)")

        snapshots = NizanimFormFiller().fill_form(form_fields=current_config, submit=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Done!")
        if len(snapshots) > 0:
            for photo_path in snapshots:
                with open(photo_path, 'rb') as photo:
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
                with open(photo_path, 'rb') as photo:
                    telegram_send.send(conf='master.conf', images=[photo])
                os.remove(photo_path)
        log_message(
            f"{child_first_name} - Finished filling form for {current_config['child_first_name']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, this is not a valid command. try: fill")
        log_message(
            f"{child_first_name} - invalid command")

def fill_really(update, context):
    log_message(f"{child_first_name} - recieved message " \
                  f"from: {update.message.from_user['first_name']} {update.message.from_user['last_name']} " \
                  f"at time: {str(update.message.date)} with: {update.message.text}")

    if is_msg_too_old(update.message.date):
        logging.info(
            f"Message too old. Do nothing")
        return
    if update.message.text.lower() == 'fill':
        log_message(f"{child_first_name} - Filling a form for {current_config['child_first_name']}")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"OK, Filling a form for {current_config['child_first_name']} :)")
        snapshots = ReallyFormFiller().fill_form(form_fields=current_config, submit=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Done!")
        if len(snapshots) > 0:
            for photo_path in snapshots:
                with open(photo_path, 'rb') as photo:
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
                with open(photo_path, 'rb') as photo:
                    telegram_send.send(conf='master.conf', images=[photo])
                os.remove(photo_path)
        log_message(
            f"{child_first_name} - Finished filling form for {current_config['child_first_name']}")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, this is not a valid command. try: fill")
        log_message(
            f"{child_first_name} - invalid command")

def fill_education_web_top(update, context):
    log_message(f"{child_first_name} - recieved message " \
                f"from: {update.message.from_user['first_name']} {update.message.from_user['last_name']} " \
                f"at time: {str(update.message.date)} with: {update.message.text}")

    if is_msg_too_old(update.message.date):
        logging.info(
            f"Message too old. Do nothing")
        return
    if update.message.text.lower() == 'fill':
        log_message(f"{child_first_name} - Filling a form for {current_config['parent_name']}")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"OK, Filling a form for {current_config['parent_name']} :)")
        snapshots = EducationWebTopFormFiller().fill_form(form_fields=current_config, submit=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Done!")
        if len(snapshots) > 0:
            for photo_path in snapshots:
                with open(photo_path, 'rb') as photo:
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
                with open(photo_path, 'rb') as photo:
                    telegram_send.send(conf='master.conf', images=[photo])
                os.remove(photo_path)
        log_message(
            f"{child_first_name} - Finished filling form for {current_config['parent_name']}")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, this is not a valid command. try: fill")
        log_message(
            f"{child_first_name} - invalid command")

def fill_kesem(update, context):
    log_message(f"{child_first_name} - recieved message from: {update.message.from_user['first_name']} " \
                  f"{update.message.from_user['last_name']} with: {update.message.text}")
    split_text = update.message.text.split()
    if len(split_text) == 2 and split_text[0].lower() == 'fill' and split_text[1].replace('.','',1).isdigit():
        temperature=split_text[1]
        if float(temperature) > max_temp:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'temperature {temperature} is too high')
            log_message(
                f"{child_first_name} - send message to: {update.message.chat['first_name']} {update.message.chat['last_name']} with: 'temperature {temperature} is too high'")
            return
        elif float(temperature) < min_temp:
            print()
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'temperature {temperature} is too low')
            log_message(
                f"{child_first_name} - send message to: {update.message.chat['first_name']} {update.message.chat['last_name']} with: 'temperature {temperature} is too low'")
            return
        log_message(f"{child_first_name} - filling a form for {current_config['child_name']} with temperature: {split_text[1]}")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"OK, filling a form for {current_config['child_name']} with temperature: {split_text[1]}")
        current_config['child_temperature'] = temperature
        snapshots = KasumFormFiller().fill_form(form_fields=current_config, submit=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Done!")
        if len(snapshots) > 0:
            for photo_path in snapshots:
                with open(photo_path, 'rb') as photo:
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
                with open(photo_path, 'rb') as photo:
                    telegram_send.send(conf='master.conf', images=[photo])
                os.remove(photo_path)
        log_message(
            f"{child_first_name} - Finished filling form for {current_config['child_name']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please use the form: fill 36.7")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Or any temperature between {min_temp} and {max_temp}")
        log_message(
            f"{child_first_name} - invalid command")

def start_w_deperature(update, context):
    logging.info(f"{child_first_name} - recieved message from: {update.message.chat['first_name']} {update.message.chat['last_name']} with: {update.message.text}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, to fill a form type: fill 36.7")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Or any temperature between {min_temp} and {max_temp}")

def start_no_temperature(update, context):
    logging.info(f"{child_first_name} - recieved message from: {update.message.chat['first_name']} {update.message.chat['last_name']} with: {update.message.text}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, to fill a form type: fill")

if __name__ == '__main__':

    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("--name", required=True,
                    help="first operand")
    args = vars(ap.parse_args())
    child_first_name = args['name']

    date = strftime("%d_%m_%Y_%H_%M_%S", gmtime())
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    handler = logging.FileHandler(f"logs/log_{child_first_name}_{date}")
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    telegram_cfg = configparser.ConfigParser()
    telegram_cfg.read(f"{child_first_name}.conf")

    token = telegram_cfg['telegram']['token']
    config = {'noam': {'child_name': 'noam',
                       'hebrew_child_name': 'נועם',
                       'hebrew_parent_name': 'נגה ואופיר גולן',
                       'type': 'kasum'},
              'noa': {'child_name': 'noa',
                      'hebrew_child_name': 'נועה',
                      'hebrew_parent_name': 'דוד והדס קאהן',
                      'type': 'kasum'},
              'maya': {'child_first_name': 'maya',
                       'child_last_name': 'indelman',
                       'hebrew_child_first_name': 'מאיה',
                       'hebrew_child_last_name': 'אינדלמן',
                       'hebrew_parent_name': 'ודים והדה אינדמן',
                       'type': 'really',
                       'child_id': '330413428',
                       'phone_number': '0544838975'},
              'noga': {'child_first_name': 'noga',
                       'child_last_name': 'indelman',
                       'hebrew_child_first_name': 'נגה',
                       'hebrew_child_last_name': 'אינדלמן',
                       'hebrew_parent_name': 'ודים והדה אינדמן',
                       'type': 'nizanim',
                       'child_id': '343056016',
                       'phone_number': '0544838975',
                       'email': 'indelman@gmail.com'},
              'moshe': {'child_first_name': 'moshe',
                        'parent_name': 'moshe',
                        'type': EducationWebTopFormFiller,
                        'user_name': '4135457',
                        'password': '9921',
                        'parent_id': '015526122'
                        }
              }
    current_config = config[child_first_name]

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    if current_config['type'] == 'kasum':
        echo_handler = MessageHandler(Filters.text & (~Filters.command), fill_kesem)
        dispatcher.add_handler(echo_handler)
        fill_handler = CommandHandler('start', start_w_deperature)
        dispatcher.add_handler(fill_handler)
    elif current_config['type'] == 'really':
        fill_handler = MessageHandler(Filters.text & (~Filters.command), fill_really)
        dispatcher.add_handler(fill_handler)
        fill_handler = CommandHandler('start', start_no_temperature)
        dispatcher.add_handler(fill_handler)
    elif current_config['type'] == 'nizanim':
        fill_handler = MessageHandler(Filters.text & (~Filters.command), fill_nizanim)
        dispatcher.add_handler(fill_handler)
        fill_handler = CommandHandler('start', start_no_temperature)
        dispatcher.add_handler(fill_handler)
    elif isinstance(current_config['type'], EducationWebTopFormFiller):
        fill_handler = MessageHandler(Filters.text & (~Filters.command), fill_education_web_top)
        dispatcher.add_handler(fill_handler)
        fill_handler = CommandHandler('start', start_no_temperature)
        dispatcher.add_handler(fill_handler)


    logging.info(f'starting bot for {child_first_name}')
    updater.start_polling()