# coding=utf-8
import os
import csv, xlrd, openpyxl.reader.excel as xlsx
from django import forms
from django.template.defaultfilters import filesizeformat
from django.conf import settings
from .models import Order, parse_quantity

def upload_parse_xls(file):
    contents = file.read()
    rb = xlrd.open_workbook(file_contents=contents,formatting_info=True)
    sheet = rb.sheet_by_index(0)
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        yield row[0], row[1]

def upload_parse_xlsx(file):
    wb = xlsx.load_workbook(file)
    sheet = wb.worksheets[0]
    for rownum in xrange(len(sheet.rows)):
        row = sheet.rows[rownum]
        yield row[0].value, row[1].value

def upload_parse_csv(file):
    dialect = csv.Sniffer().sniff(file.read())
    reader = csv.reader(file, dialect=dialect)
    for row in reader:
        yield row[0], row[1]

UPLOAD_PARSERS = {
    '.xls': upload_parse_xls,
    '.xlsx': upload_parse_xlsx,
    '.csv': upload_parse_csv,
}

def upload_parse(file, file_ext):
    result = []
    for part_number, quantity in UPLOAD_PARSERS[file_ext](file):
        try:
            item = part_number, parse_quantity(quantity)
        except Exception:
            pass
        else:
            result.append(item)
    return result

UPLOAD_PARSERS_FORMAT = u", ".join(UPLOAD_PARSERS.keys())
UPLOAD_MAX_SIZE_FORMAT = filesizeformat(settings.ORDER_UPLOAD_MAX_SIZE)

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = 'payment_type', 'comment',


class UploadFileForm(forms.Form):
    file = forms.FileField(label=u"Файл", help_text=u"Расширение - {}. Не более {}.".format(UPLOAD_PARSERS_FORMAT, UPLOAD_MAX_SIZE_FORMAT))

    def clean_file(self):
        file = self.cleaned_data['file']
        file_name, file_ext = os.path.splitext(file.name)
        if file.size > settings.ORDER_UPLOAD_MAX_SIZE:
            raise forms.ValidationError(u"Слишком большой размер файла ({}). Максимальный размер - {}.".format(filesizeformat(file.size), UPLOAD_MAX_SIZE_FORMAT))
        elif file_ext not in UPLOAD_PARSERS.keys():
            raise forms.ValidationError(u"Недопустимый тип файла, необходимо загружать только {} файлы.".format(UPLOAD_PARSERS_FORMAT))

        return upload_parse(file, file_ext)
