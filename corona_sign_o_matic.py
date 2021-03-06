import io
import pdfrw
from reportlab.pdfgen import canvas
from time import gmtime, strftime

from telegram_utils import send_pdf_over_telegram
import os
import random


def run_batch():
    Year = "2020"
    Month = [5, 7]
    Days = [1, 31]
    for month in range(Month[0], Month[1] + 1):
        for day in range(Days[0], Days[1] + 1):
            date = "{}.{}.{}".format(day, month, Year)
            reversed_date = "{}.{:02d}.{:02d}".format(Year, month, day)
            # date = strftime("%d.%m.%Y", gmtime())
            canvas_data = get_overlay_canvas(date)
            form = merge(canvas_data, template_path='templates/health_decleration_peleg.pdf')
            filename = './media/health_decleration_{}.pdf'.format(reversed_date)
            save(form, filename=filename)
            # send_pdf_over_telegram(filename)


def run_hador_haba(conf):
    date = strftime("%d.%m.%Y", gmtime())
    canvas_data = get_overlay_canvas(date, conf['type'])
    form = merge(canvas_data, template_path='./templates/health_decleration_{}.pdf'.format(conf['child_name']))
    filename = './media/health_decleration_{}_{}.pdf'.format(conf['child_name'], date)
    save(form, filename=filename)
    send_pdf_over_telegram(conf['child_name'], filename)
    os.remove(filename)


def run_saar(conf):
    date = strftime("%d.%m.%Y", gmtime())
    canvas_data = get_overlay_canvas(date, conf['type'])
    form = merge(canvas_data, template_path='./templates/health_decleration_{}.pdf'.format(conf['child_name']))
    filename = './media/health_decleration_{}_{}.pdf'.format(conf['child_name'], date)
    save(form, filename=filename)
    send_pdf_over_telegram(conf['child_name'], filename)
    os.remove(filename)


def run(conf):
    if conf['type'] == 'hador_haba':
        run_hador_haba(conf)
    elif conf['type'] == 'saar':
        run_saar(conf)


def get_overlay_canvas(date, type) -> io.BytesIO:
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    if type == 'hador_haba':
        random_shift = random.randint(1, 50)
        pdf.drawString(x=100 + random_shift, y=205, text=date)
        random_shift = random.randint(1, 50)
        pdf.drawString(x=100 + random_shift, y=255, text=date)
    elif type == 'saar':
        random_shift = random.randint(1, 10)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFontSize(size=15)
        pdf.drawString(x=210 + random_shift, y=180, text=date)

    pdf.save()
    data.seek(0)
    return data


def merge(overlay_canvas: io.BytesIO, template_path: str) -> io.BytesIO:
    template_pdf = pdfrw.PdfReader(template_path)
    overlay_pdf = pdfrw.PdfReader(overlay_canvas)
    for page, data in zip(template_pdf.pages, overlay_pdf.pages):
        overlay = pdfrw.PageMerge().add(data)[0]
        pdfrw.PageMerge(page).add(overlay).render()
    form = io.BytesIO()
    pdfrw.PdfWriter().write(form, template_pdf)
    form.seek(0)
    return form


def save(form: io.BytesIO, filename: str):
    with open(filename, 'wb') as f:
        f.write(form.read())


if __name__ == '__main__':
    conf_list = [{'child_name': 'peleg', 'type': 'hador_haba'},
                 {'child_name': 'saar', 'type': 'saar'}
                 ]

    for conf in conf_list:
        run(conf)
