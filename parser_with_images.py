import requests
import lxml.html
import csv
import time
import math
import os
from PIL import Image
import re


html = requests.get('https://krisha.kz/arenda/kommercheskaya-nedvizhimost/almaty-alatauskij/')
doc = lxml.html.fromstring(html.content)

pagination = doc.xpath('//nav[@class="paginator"]')[0]
last_page = pagination.xpath('.//a/text()')[-4]
last_page = int(last_page)
print(last_page)


iter = 1
header = ['Ссылка', 'Заголовок', 'Сумма за месяц', 'Сумма за кв.м.', 'Автор объявления', 'Город', 'Этаж', 'Адрес', 'Площадь объекта, м²', 'Размещение объекта', 'Состояние', 'Линия домов', 'Коммуникации', 'Вход', 'Год постройки', 'Высота потолков', 'Действующий бизнес', 'Безопасность', 'Парковка', 'Название объекта', 'Выделенная мощность, кВт', 'Путь к картинкам', 'Описание']

with open('output.tsv', 'a') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(['Ссылка', 'Заголовок', 'Сумма за месяц', 'Сумма за кв.м.', 'Автор объявления', 'Город', 'Этаж', 'Адрес', 'Площадь объекта, м²', 'Размещение объекта', 'Состояние', 'Линия домов', 'Коммуникации', 'Вход', 'Год постройки', 'Высота потолков', 'Действующий бизнес', 'Безопасность', 'Парковка', 'Название объекта', 'Выделенная мощность, кВт', 'Путь к картинкам', 'Описание'])

while iter <= last_page:
    html = requests.get('https://krisha.kz/arenda/kommercheskaya-nedvizhimost/almaty-medeuskij/?das[rent.square]=2&page='+str(iter))
    doc = lxml.html.fromstring(html.content)

    section = doc.xpath('//section[@class="a-list a-search-list a-list-with-favs"]')[0]

    anns = section.xpath('.//div[@data-id]')
    iter_ann = 1
    for ann in anns:
        rows = {}
        page = ann.xpath('.//div/a/@href')[0]
        print(page)
        page_html = requests.get('https://krisha.kz'+page)
        page_doc = lxml.html.fromstring(page_html.content)
        layout = page_doc.xpath('//div[@class="layout__content"]')[0]
        page_url = "https://krisha.kz"+page
        rows['Ссылка'] = page_url

        title = layout.xpath('.//div[@class="offer__advert-title"]/h1/text()')[0] if layout.xpath('.//div[@class="offer__advert-title"]/h1/text()') else ""
        rows['Заголовок'] = title

        sidebar = layout.xpath('.//div[@class="offer__sidebar"]')[0]
        price = sidebar.xpath('.//div[@class="offer__price"]/text()') if sidebar.xpath('.//div[@class="offer__price"]/text()') else ""

        total_price = ""

        for p in price:
            if p!=" ":
                total_price+=p
        total_price = total_price.replace(" ", "")
        total_price = total_price.split("\n")

        total_price = list(filter(None, total_price))
        total_price = list(map(lambda x: x.replace(u'\xa0', u''), total_price))

        month_price = total_price[0]
        square_price = total_price[1]
        rows['Сумма за месяц'] = month_price
        rows['Сумма за кв.м.'] = square_price

        author1 = "".join(sidebar.xpath('.//div[@class="owners__name owners__name--large"]/text()')) if sidebar.xpath('.//div[@class="owners__name owners__name--large"]/text()') else ""
        author2 = "".join(sidebar.xpath('.//div[@class="label label--transparent label-user-identified-specialist"]/text()')) if sidebar.xpath('.//div[@class="label label--transparent label-user-identified-specialist"]/text()') else ""
        author_total = author1 + author2
        author_total = author_total.strip()
        print(author_total)

        rows['Автор объявления'] = author_total


        short_desc = sidebar.xpath('.//div[@class="offer__short-description"]')[0] if sidebar.xpath('.//div[@class="offer__short-description"]') else ""
        for s in short_desc:
            k = "".join(s.xpath('.//div[@class="offer__info-title"]/text()'))
            v1 = "".join(s.xpath('.//div[@class="offer__location offer__advert-short-info"]/span/text()'))
            v2 = "".join(s.xpath('.//div[@class="offer__advert-short-info"]/text()'))
            v_total = v1+v2
            #print(k, v_total)
            rows[k] = v_total




        content = layout.xpath('.//div[@class="offer__content"]')[0]
        parameters = content.xpath('.//div[@class="offer__parameters"]')[0] if content.xpath('.//div[@class="offer__parameters"]') else ""

        for param in parameters:
            k = "".join('.//dt/text()')
            v = "".join('.//dd/text()')
            print(k, v)
            rows[k] = v


        images = content.xpath('.//ul[@class="gallery__small-list"]/li') if content.xpath('.//ul[@class="gallery__small-list"]/li') else []
        pictures = []
        for img in images:
            pictures.append(img.xpath('.//div/@data-photo-url')[0])

        dir = str(iter)+"/"+str(iter_ann)
        os.makedirs(dir)
        i = 0
        for p in pictures:

            img_url = p
            response = requests.get(img_url)
            completeName = os.path.join(dir, str(i)+".jpg")
            print(completeName)
            with open(completeName, "wb") as f:

                f.write(response.content)
            i+=1

        rows['Путь к картинкам'] = completeName

        if content.xpath('.//div[@class="text"]'):
            text = content.xpath('.//div[@class="text"]')[0]
            description = "".join(text.xpath('.//div[@class="a-text a-text-white-spaces"]/text()'))
        else:
            description = ""
        rows['Описание'] = description

        row = []
        isEmpty = True
        for h in header:
            for k, v in rows.items():
                if k == h:
                    row.append(v)
                    isEmpty = False
            if isEmpty:
                row.append(" ")
            else:
                isEmpty = True



        with open('output.tsv', 'a') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow(row)

        iter_ann+=1




    print(iter)
    iter+=1
