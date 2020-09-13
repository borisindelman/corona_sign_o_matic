import telegram_send

def send_pdf_over_telegram(conf_name, filepath):
    with open(filepath, "rb") as f:
        telegram_send.send(conf='conf/{}.conf'.format(conf_name), files=[f])

def send_job_done(conf_name):
    telegram_send.send(conf='conf/{}.conf'.format(conf_name), messages=['job done'])