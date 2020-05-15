import telegram_send
# 1155610601:AAE_OhPX9n0liQad-AoJ4UDC26O5DmiIu-I
# lkdfhglkdjfnvlduvdvfnfvbot

def send_pdf_over_telegram(filepath):
    with open(filepath, "rb") as f:
        telegram_send.send(files=[f])
