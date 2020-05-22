from jinja2 import Template
import pdfkit
from datetime import datetime
from locale import setlocale, LC_ALL
from decimal import Decimal
from num2t4ru import decimal2text

# установка локали для вывода месяца из datetime на русском
setlocale(LC_ALL, 'ru_ru.UTF-8')

path_to_template_html = "template.html"
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
path_to_out_pdf = 'bill.pdf'

# подключение wkhtmltopdf к pdfkit
try:
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
except:
    print('Не удалось найти wkhtmltopdf по пути:', path_to_wkhtmltopdf)
    exit(-1)
# инициализация шаблона
try:
    html = open(path_to_template_html, encoding='utf8').read()
except:
    print('Не удалось найти HTML-шаблон по пути:', path_to_template_html)
    exit(-1)
template = Template(html)

date_account = datetime.today()
date_account = date_account.strftime('%d %B')[:-1] + 'я ' + date_account.strftime('%Y') + 'г.'

price = {
    'internet': 1,
    'sms':      1,
    'call':     {'in': 1,    'out': 1}
}
count = {
    'internet': 8497.25,
    'sms':      13,
    'call':     {'in': 7.52, 'out': 85.7}
}
price_s = {
    'internet': 7497.25,
    'sms':      8,
    'call':     {'in': 7.52,  'out': 85.7}
}
cond = {
    'internet': ['1000 кб бесплатно', ' руб/кб'],
    'sms':      ['5 SMS бесплатно', ' руб/SMS'],
    'call':     {'in': ['Плата за исходящие звонки', ' руб/мин'],
                 'out': ['Плата за входящие звонки', ' руб/мин']}
}

price_s_all = '{:.2f}'.format(price_s['internet']+price_s['sms']+price_s['call']['in']+price_s['call']['out'])
NDS = float(price_s_all) * 0.18
price_s_all_text = decimal2text(Decimal(price_s_all),
                                places=2,
                                int_units=((u'рубль', u'рубля', u'рублей'), 'm'),
                                exp_units=((u'копейка', u'копейки', u'копеек'), 'f')
                                )
price_s_all_text = price_s_all_text[0].upper() + price_s_all_text[1:]

# словарь данных для подстановки в словарь
template_dict = {
    'dest_bank': 'ПАО "БабахБанк", Г. С4', 'bik_bank': '2288841', 'dest_account_bank': '04875748474843469',
    'settlment_account': '00587312133865897', 'INN': '90770973', 'KPP': '0001309753',
    'org_name': 'ООО "Министерство Магии"',
    'n_number': -1, 'n_datetime': date_account,
    'contractor': 'ООО "Министерство Магии", ИНН 90770973, КПП 4947643111,'
                  'г. Лондон, ТогокогоНН ул., дом 3/4, тел.: 62442',
    'buyer': 'Мальчик К.В., ИНН 12345678, КПП 9876543210, Годрикова Падь',
    'osn_number': 'NULL', 'osn_date': '01.01.2000',
    'cond_telephony_in': cond['call']['in'][0], 'price_telephony_in': str(price['call']['in'])+cond['call']['in'][1],
        'count_telephony_in': count['call']['in'], 'price_telephony_s_in': price_s['call']['in'],
    'cond_telephony_out': cond['call']['out'][0], 'price_telephony_out': str(price['call']['out'])+cond['call']['out'][1],
        'count_telephony_out': count['call']['out'], 'price_telephony_s_out': price_s['call']['out'],
    'cond_sms': cond['sms'][0], 'price_sms': str(price['sms'])+cond['sms'][1],
        'count_sms': count['sms'], 'price_sms_s': price_s['sms'],
    'cond_internet': cond['internet'][0], 'price_internet': str(price['internet'])+cond['internet'][1],
        'count_internet': count['internet'], 'price_internet_s': price_s['internet'],
    'NDS': NDS, 'price_s_all': price_s_all, 'price_s_in_letter': price_s_all_text,
    'ruk_fio': 'Руководителев Ф.Ф.', 'len_ruk_fio': len('Руководителев Ф.Ф.'),
    'gl_bux_fio': 'Бухгалтерова Ф.Ф.', 'len_gl_bux_fio': len('Бухгалтерова Ф.Ф.'),
}

try:
    filled_template = template.render(template_dict)
except:
    print('Не удалось заполнить шаблон (наиболее часто это происходит при неправильном заполнении template_dict')
    exit(-1)
try:
    pdfkit.from_string(filled_template, path_to_out_pdf, configuration=config, options={'quiet': ''})
except:
    print('Не удалось сохранить счет по пути:', path_to_out_pdf, '(возможно файл заблокирован)')
    exit(-1)
print('Счет на оплату услуг успешно сгенерирован')