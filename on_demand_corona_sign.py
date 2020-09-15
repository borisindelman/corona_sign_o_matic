import argparse
import importlib
import json
import os
import sys
from datetime import datetime, timezone
from time import strftime, gmtime
import re

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import configparser
import logging
import telegram_send

submit_value = True

min_temp = 36
max_temp = 38
max_msg_time = 60 * 5


def is_msg_too_old(update, context):
    is_too_old = (datetime.now(timezone.utc) - update.message.date).seconds > max_msg_time
    if is_too_old:
        send_message(update=update, context=context, message="I'm sorry, my server was down :/ \n"
                                                             "What would you like me to do?")
    return is_too_old


def log_message(message):
    logging.info(message)
    telegram_send.send(conf='conf/master.conf',
                       messages=[str(datetime.now().strftime('%m/%d/%Y %H:%M:%S')) + ' - ' + message])


def utc_to_local(time):
    return time.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%m/%d/%Y %H:%M:%S')


def log_new_message(update, is_received: bool):
    log_message(f"{bot_name}_bot - {'received' if is_received else 'sent'} message "
                f"{'from' if is_received else 'to'}: "
                f"{update.message.from_user['first_name']} {update.message.from_user['last_name']} "
                f"at time: {str(utc_to_local(update.message.date))} "
                f"with: {update.message.text}")


def log_received_message(update):
    log_new_message(update=update, is_received=True)


def log_sent_message(update):
    log_new_message(update=update, is_received=False)


def send_snapshots(snapshots, update, context):
    if len(snapshots) > 0:
        for photo_path in snapshots:
            with open(photo_path, 'rb') as photo:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
            with open(photo_path, 'rb') as photo:
                telegram_send.send(conf='conf/master.conf', images=[photo])
            os.remove(photo_path)


def send_message(update, context, message: str):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    log_sent_message(update=update)


def fill_form_handler(update, context):
    filler_class = current_config['type']()
    log_received_message(update=update)
    if is_msg_too_old(update, context):
        return
    if filler_class.is_temperature_required:
        split_text = update.message.text.split()
        condition = (len(split_text) == 2 and split_text[0].lower() == 'fill' and split_text[1].replace('.', '', 1).isdigit())
    else:
        condition = update.message.text.lower() == 'fill'

    if condition:
        if filler_class.is_temperature_required:
            temperature = split_text[1]
            if not is_temperature_in_limits(update, context, temperature):
                return
            send_message(update=update, context=context,
                         message=f"OK, filling a form for {current_config['child_first_name'].title()} "
                                 f"with temperature: {split_text[1]}")        
            current_config['child_temperature'] = temperature
        else:
            send_message(update=update, context=context,
                         message=f"OK, Filling a form for {current_config['child_first_name'].title()} :)")
        snapshots = filler_class.fill_form(form_fields=current_config, submit=submit_value)
        if len(snapshots) < (filler_class.expected_snapshots if submit_value else filler_class.debug_snapshots):
            send_message(update=update, context=context, message="I'm sorry, something went wrong. \n"
                                                                 "Please try again or contact Boris.")
            return
        send_message(update=update, context=context, message="Done!")
        send_snapshots(snapshots, update, context)
        log_message(f"{bot_name}_bot - Finished filling form for {current_config['child_first_name'].title()}")
    else:
        if filler_class.is_temperature_required:
            send_message(update=update, context=context, message="Please use the form: fill 36.7 \n"
                                                                 f"Or any temperature between {min_temp} and {max_temp}")
        else:
            send_message(update=update, context=context, message="Sorry, this is not a valid command. try: fill")


def is_temperature_in_limits(update, context, temperature):
    if float(temperature) > max_temp:
        send_message(update=update, context=context, message=f'temperature {temperature} is too high')
        return False
    elif float(temperature) < min_temp:
        send_message(update=update, context=context, message=f'temperature {temperature} is too low')
        return False
    return True


def start_form_handler(update, context):
    filler_class = current_config['type']()
    log_received_message(update=update)
    if filler_class.is_temperature_required:
        send_message(update=update, context=context, message="Hi, to fill a form type: fill 36.7 \n"
                                                             f"Or any temperature between {min_temp} and {max_temp}")
    else:
        send_message(update=update, context=context, message="Hi, to fill a form type: fill")
    send_message(update=update, context=context, message=f"To set a daily reminder type /reminder")


def set_logger(bot_name: str):
    date = strftime("%d_%m_%Y_%H_%M_%S", gmtime())
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt="%m/%d/%Y %H:%M:%S")
    handler.setFormatter(formatter)
    root.addHandler(handler)

    handler = logging.FileHandler(f"logs/log_{bot_name}_{date}")
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    root.addHandler(handler)


def reminder_fill_handler(update, context):
    user_name = f"{update.message.from_user['first_name']}_{update.message.from_user['last_name']}"
    chat_id = update.effective_chat.id
    if os.path.isfile('reminder_list.json'):
        with open('reminder_list.json', 'r') as fp:
            reminder_list = json.load(fp)
    else:
        reminder_list = {}

    if user_name in reminder_list:
        del reminder_list[user_name]
        send_message(update=update, context=context, message="OK, Removing your daily reminder.")
    else:
        reminder_list[user_name] = {'bot_name': bot_name, 'chat_id': chat_id, 'time': '07:00'}
        send_message(update=update, context=context, message="OK, I'm setting up a daily reminder fo you :)")
    with open('reminder_list.json', 'w') as fp:
        json.dump(reminder_list, fp)


def get_bot_token(bot_name: str):
    telegram_cfg = configparser.ConfigParser()
    telegram_cfg.read(f"conf/{bot_name}.conf")
    return telegram_cfg['telegram']['token']


def create_bot(bot_name: str, telegram_cfg):
    token = telegram_cfg['token']
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    snake_case_class_name = re.sub(r'(?<!^)(?=[A-Z])', '_', current_config['type']).lower()
    module = importlib.import_module('fillers.' + snake_case_class_name)
    current_config['type'] = getattr(module, current_config['type'])

    echo_handler = MessageHandler(Filters.text & (~Filters.command), fill_form_handler)
    dispatcher.add_handler(echo_handler)
    fill_handler = CommandHandler('start', start_form_handler)
    dispatcher.add_handler(fill_handler)
    reminder_handler = CommandHandler('reminder', reminder_fill_handler)
    dispatcher.add_handler(reminder_handler)
    log_message(f'starting {bot_name}_bot')
    updater.start_polling()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    # Add the arguments to the parser
    ap.add_argument("--name", required=True,
                    help="first operand")
    args = vars(ap.parse_args())
    bot_name = args['name']

    cfg = configparser.ConfigParser()
    conf_path = os.path.join('conf', f"{bot_name}.conf")
    assert os.path.isfile(conf_path), f"unrecognized bot name: {bot_name}"

    cfg.read(f"conf/{bot_name}.conf")

    current_config = cfg._sections['filler']
    set_logger(bot_name=bot_name)

    create_bot(bot_name=bot_name, telegram_cfg=cfg['telegram'])



# config = {'noam': {'child_first_name': 'noam',
#                    'hebrew_child_first_name': 'נועם',
#                    'hebrew_parent_name': 'נגה ואופיר גולן',
#                    'type': KasumFormFiller},
#           'noa': {'child_first_name': 'noa',
#                   'hebrew_child_first_name': 'נועה',
#                   'hebrew_parent_name': 'דוד והדס קאהן',
#                   'type': KasumFormFiller},
#           'maya': {'child_first_name': 'maya',
#                    'child_last_name': 'indelman',
#                    'hebrew_child_first_name': 'מאיה',
#                    'hebrew_child_last_name': 'אינדלמן',
#                    'hebrew_parent_name': 'ודים והדה אינדמן',
#                    'type': ReallyFormFiller,
#                    'child_id': '330413428',
#                    'phone_number': '0544838975'},
#           'noga': {'child_first_name': 'noga',
#                    'child_last_name': 'indelman',
#                    'hebrew_child_first_name': 'נגה',
#                    'hebrew_child_last_name': 'אינדלמן',
#                    'hebrew_parent_name': 'ודים והדה אינדמן',
#                    'type': NizanimFormFiller,
#                    'child_id': '343056016',
#                    'phone_number': '0544838975',
#                    'email': 'indelman@gmail.com'},
#           'zohar': {'child_first_name': 'zohar',
#                     'parent_name': 'moshe',
#                     'type': EducationWebTopFormFiller,
#                     'user_name': '4135457',
#                     'password': '9921',
#                     'parent_id': '015526122'
#                     },
#           'yuval': {'child_first_name': 'yuval',
#                     'parent_name': 'moshe',
#                     'type': EducationWebTopFormFiller,
#                     'user_name': '4401087',
#                     'password': '6197',
#                     'parent_id': '015526122'
#                     },
#           'yonatan': {'child_first_name': 'yonatan',
#                       'parent_name': 'netali',
#                       'type': EducationGanFormFiller,
#                       'user_name': '039339353',
#                       'password': 'Yonatan2701',
#                       }
#           }
