# -*- coding: utf-8 -*-

import json
import pandas as pd
import pages.data
import pages.image
import os
import platform

URL = "http://novotechnic.ru"
DOMEN = "novotechnic.ru"

def make_directories():
    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists('json'):
        os.makedirs('json')

def make_csv(goods):
    csv = "name;artikul;model;manufacturer;description;image;price;link\n"
    for good in goods:
        good = json.loads(good)
        csv += (good[0]['name'] + ";"
                + good[0]['artikul'] + ";"
                + good[0]['model'] + ";"
                + good[0]['manufacturer'] + ";"
                + good[0]['description'] + ";"
                + good[0]['image'] + ";"
                + good[0]['price'] + ";"
                + good[0]['link'] + "\n")
    return csv

def get_image_url(page, css_class):
    try:
        info = pages.data.get_tag(page, 'div', css_class)
        return info.find('a', 'cloud-zoom').attrs.get('href')
    except:
        return None

def get_description(page, css_class):
    try:
        return pages.data.get_tag(page, 'div', css_class)
    except:
        return None

def get_parameters(description):
    try:
        parameters = description.text
        parameters = parameters.replace(' ', '')
        parameters = parameters.replace(';', '')
        parameters = parameters.split('\n')
        parameters = list(filter(None, parameters))
        return parameters
    except:

        return None

def get_price(page, css_class):
    try:
        price = pages.data.get_tag(page, 'div', css_class).text
        price = price.replace(' ', '')
        price = price.replace(';', '')
        price = price.split('\n')
        price = list(filter(None, price))
        return float(price[1].replace('р.',''))
    except:
        return None

def get_product_description(page):
    try:
        product_description = pages.data.get_tag(page, 'div', 'tab-content').text
        product_description = string_replace(product_description)
        return product_description
    except:
        return None

def string_replace(str):
    str = str.replace('"', '')
    str = str.replace('\n', ' ')
    str = str.replace('\t', ' ')
    str = str.replace(';', '.')
    return str

def parse_page(page):
    try:
        name = pages.data.get_tag(page, 'h1', '').text
        name = string_replace(name)
        description = get_description(page, 'description')
        product_description = get_product_description(page)
        image_url = get_image_url(page, 'product-info')
        filename = image_url[image_url.rfind('/') + 1:]
        image_filename = 'images/' + image_url[image_url.rfind('/') + 1:]
        filename = filename[:filename.rfind('.')]
        pages.image.save_image(image_url, image_filename)
        parameters = get_parameters(description)
        manufacturer = ''
        artikul = ''
        model = ''
        for parameter in parameters:
            if parameter.find('Производитель') >= 0:
                manufacturer = parameter[parameter.find(':') + 1:]
            if parameter.find('Артикул') >= 0:
                artikul = parameter[parameter.find(':') + 1:]
            if parameter.find('Модель') >= 0:
                model = parameter[parameter.find(':') + 1:]
        if artikul == '':
            artikul = model
        price = get_price(page, 'price')
        json = ('[{"name":"' + name
                + '", "artikul":"' + artikul
                + '", "model":"' + model
                + '", "manufacturer":"' + manufacturer
                + '", "description":"' + str(product_description)
                + '", "image":"' + image_filename
                + '", "price":"' + str(price)
                + '", "link":"' + image_url + '"}]')
        pages.image.save_file(json, 'json/' + filename + '.json', "w")
        return (json)
    except:
        return None

def main():
    make_directories()
    down = []

    page = pages.data.get_page(URL)
    links = pages.data.get_child_urls(page)
    links_categories = []
    links_goods = []
    for link in links:
        if link.find(DOMEN) >= 0 and link.find('?') < 0 and link != URL:
            if not link in down:
                child_page = pages.data.get_page(link)
                if pages.data.is_page_matched(child_page, 'div', 'category-info'):
                    links_categories.append(link)
                    child_page_links = pages.data.get_child_urls(child_page)
                    for child_link in child_page_links:
                        if (child_link.find(DOMEN) >= 0
                                and child_link.find('?') < 0
                                and child_link != URL
                                and not child_link in links_goods):
                            links_goods.append(child_link)
                else:
                    if not pages.data.is_page_matched(child_page, 'div', 'product-info'):
                        down.append(link)

    for link in down:
        if link in links_goods:
            list.remove(links_goods, link)
    for link in links_categories:
        if link in links_goods:
            list.remove(links_goods, link)

    goods = []
    for link in links_goods:
        page = pages.data.get_page(link)
        if pages.data.is_page_matched(page, 'div', 'product-info'):
            goods.append(parse_page(page))

    pages.image.save_file(str(goods), 'result.json', 'w')

    csv = make_csv(goods)

    try:
        pages.image.save_file(csv, 'result.csv', 'w')
        df = pd.read_csv('result.csv', sep=';', encoding='windows-1251')
        df.to_excel('result.xlsx')
    except:
        None

if __name__ == '__main__':
    main()
