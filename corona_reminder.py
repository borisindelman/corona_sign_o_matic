import configparser
import json

import telegram

if __name__ == '__main__':
    with open('reminder_list.json', 'r') as fp:
        reminder_list = json.load(fp)
    for key,value in reminder_list.items():
        cfg = configparser.ConfigParser()
        cfg.read(f"conf/{value['bot_name']}.conf")
        bot = telegram.bot.Bot(token=cfg['telegram']['token'])
        bot.send_message(chat_id=value['chat_id'],
                         text=f"Good morning {key}. \n"
                              f"Don't forget to fill a form with the fill command :) \n"
                              f"Have a nice day.")
