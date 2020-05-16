import telegram_send

def send_pdf_over_telegram(conf_name, filepath):
    with open(filepath, "rb") as f:
        telegram_send.send(conf='{}.conf'.format(conf_name), files=[f])
