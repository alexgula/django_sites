# coding=utf-8
import os
from fpdf import FPDF
from constance import config
from . import num2text_ua

DIRNAME = os.path.dirname(os.path.realpath(__file__))
BORDER_DEBUG = 0


def asset_path(file_name):
    return os.path.join(DIRNAME, 'pdf_assets', file_name)


class Document(object):

    def __init__(self, **kwargs):
        self.pdf = FPDF(**kwargs)
        self.pdf.add_page()
        self.pdf.set_margins(20, 20, 0)
        self.pdf.ln()
        self._add_font('DejaVu', 'DejaVuSansCondensed.ttf')
        self._add_font('DejaVu-Bold', 'DejaVuSansCondensed-Bold.ttf')

    def _add_font(self, font_name, file_name):
        self.pdf.add_font(font_name, '', asset_path(file_name), uni=True)

    def _font(self, size, bold=False):
        font_name = 'DejaVu' if not bold else 'DejaVu-Bold'
        self.pdf.set_font(font_name, '', size)

    def _text_cell(self, w, h, text, size=10, bold=False, align='L', border=BORDER_DEBUG):
        self._font(size, bold=bold)
        self.pdf.cell(w, h, text, align=align, border=border)

    def _multi_cell(self, w, h, text, size=10, bold=False, align='L', border=BORDER_DEBUG):
        self._font(size, bold=bold)
        self.pdf.multi_cell(w, h, text, align=align, border=border)

    def output(self):
        return self.pdf.output(dest='S')


class Invoice(Document):

    def __init__(self, order, order_date, order_sum, **kwargs):
        super(Invoice, self).__init__(**kwargs)
        self.order = order
        self.order_date = order_date
        self.order_sum = order_sum

    def _top_row(self, head, text):
        self._text_cell(40, 5, head, bold=True)
        self._multi_cell(130, 5, text)

    def _title(self, lines):
        self.pdf.ln(12)
        for line in lines:
            self._text_cell(170, 8, line, size=16, bold=True, align='C')
            self.pdf.ln()
        self.pdf.ln(12)

    @staticmethod
    def _table_row(cols, row):
        for i, value in enumerate(row):
            col = cols[i]
            title, w, align = col[:3]
            fmt = col[3] if len(col) > 3 else u"{}"
            yield fmt.format(value), w, align

    def _table(self, cols, rows, subtitles):
        for col in cols:
            title, w, align = col[:3]
            self._text_cell(w, 5, title, bold=True, align='C', border=1)
        self.pdf.ln()

        for row in rows:
            cell_rows = [
                self.pdf.multi_cell(w, 5, text, align=align, border=1, split_only=True)
                for text, w, align in self._table_row(cols, row)
            ]
            row_count = max(len(cells) for cells in cell_rows)
            for row_i in range(row_count):
                for col_i, (_, w, align) in enumerate(self._table_row(cols, row)):
                    cells = cell_rows[col_i]
                    text = cells[row_i] if row_i < len(cells) else u""
                    border = 'LR'
                    if row_i == 0:
                        border += 'T'
                    if row_i == row_count - 1:
                        border += 'B'
                    self._text_cell(w, 5, text, align=align, border=border)
                self.pdf.ln()

        for head, text in subtitles:
            self._text_cell(140, 5, head, bold=True, align='R')
            self._text_cell(30, 5, u"{:.2f}".format(text), bold=True, border=1, align='R')
            self.pdf.ln()

    def _full_row(self, text, *args, **kwargs):
        self._multi_cell(170, 5, text, *args, **kwargs)

    def make(self):
        self._top_row(u"Постачальник", config.INVOICE_SUPPLIER)
        self._top_row(u"Одержувач", u"\n".join([self.order.customer.name, self.order.customer.phone]))
        self._top_row(u"Платник", u"той самий")
        self._top_row(u"Замовлення", u"без замовлення")

        self._title([
            u"Рахунок-фактура № I-{}".format(self.order.id),
            u"від {} р.".format(self.order_date),
        ])

        self._table([
            (u"№", 10, 'R'),
            (u"Назва", 70, 'L'),
            (u"Од.", 10, 'C'),
            (u"Кількість", 20, 'R'),
            (u"Ціна без ПДВ", 30, 'R', u"{:.2f}"),
            (u"Сума без ПДВ", 30, 'R', u"{:.2f}"),
        ], [(
            i + 1,
            item.title,
            u"шт.",
            item.quantity,
            item.price_without_pdv,
            item.sum_without_pdv,
            ) for i, item in enumerate(self.order.items.all())
        ], [
            (u"Разом без ПДВ:", self.order.sum_without_pdv),
            (u"ПДВ:", self.order.sum_of_pdv),
            (u"Всього з ПДВ:", self.order.sum_uah),
        ])
        self._full_row(u"Всього на суму:")
        self._full_row(u"{}".format(self.order_sum.capitalize()), bold=True)
        self._full_row(u"ПДВ: {:.2f} грн.".format(self.order.sum_of_pdv))
        self.pdf.ln(15)

        self._text_cell(90, 5, u"Виписав(ла):", align='R')
        self._text_cell(20, 5, u"")
        self._text_cell(60, 5, u"", border='B')
        self.pdf.ln(20)

        self._full_row(u"Рахунок дійсний до сплати до {}".format(self.order.date.strftime('%d.%m.%Y')),
                       bold=True, align='R')

        self.pdf.image(asset_path('stamp.png'), 110, self.pdf.y - 53, h=50)

        return self.output()


def invoice(order):
    result = Invoice(order, format_date_ua(order.date), format_num_ua(order.sum_uah))
    return result.make()


MONTHS_UA = [
    u"січня",
    u"лютого",
    u"березня",
    u"квітня",
    u"травня",
    u"червня",
    u"липня",
    u"серпня",
    u"вересня",
    u"жовтня",
    u"листопада",
    u"грудня",
]


def format_date_ua(date):
    return u"{:02} {} {:04}".format(date.day, MONTHS_UA[date.month - 1], date.year)


def format_num_ua(value):
    int_part = int(value)
    rem_part = int(value % 1 * 100)
    text = num2text_ua.num2text(int_part)
    return u"{} гривень {:02} копійок".format(text, rem_part)
