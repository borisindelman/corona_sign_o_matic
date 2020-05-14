import io

import pdfrw
from reportlab.pdfgen import canvas
from time import gmtime, strftime
from pdf_over_mail import send_pdf_over_mail

def run():
    date = strftime("%d.%m.%Y", gmtime())
    canvas_data = get_overlay_canvas(date)
    form = merge(canvas_data, template_path='./health_decleration.pdf')
    filename = 'health_decleration_{}.pdf'.format(date)
    save(form, filename=filename)
    send_pdf_over_mail(filename)


def get_overlay_canvas(date) -> io.BytesIO:
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    pdf.drawString(x=100, y=205, text=date)
    pdf.drawString(x=100, y=255, text=date)
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
    run()