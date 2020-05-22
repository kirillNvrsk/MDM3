Программа для генерации печатной формы счета на оплату услуг в формате PDF.
Запуск осуществляется через терминал с помощью команды python main.py

Путь к HTML шаблону задается через переменную path_to_template_html.
Путь к выходному файлу задается через переменную path_to_out_pdf.

 Зависимости:
 	pdfkit
	jinja2
	num2t4ru (https://github.com/seriyps/ru_number_to_text)
	
Также на ПК должен быть установлен wkhtmltopdf. Путь к нему необходимо прописать в переменной path_to_wkhtmltopdf

