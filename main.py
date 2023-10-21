# -*- coding: utf-8 -*-

import json
import pandas as pd
import pages.data
import pages.image
import os
import platform

URL = "http://novotechnic.ru"
DOMEN = "novotechnic.ru"

down = []
csv = "artikul;model;manufacturer;image;price;link\n"

def getImageUrl(page, css_class):
    try:
        info = pages.data.getTag(page, 'div', css_class)
        return info.find('a', 'cloud-zoom').attrs.get('href')
    except:

        return None

def getDescription(page, css_class):
    try:
        return pages.data.getTag(page, 'div', css_class)
    except:
        return None

def getParameters(description):
    try:
        parameters = description.text
        parameters = parameters.replace(' ', '')
        parameters = parameters.replace(';', '')
        parameters = parameters.split('\n')
        parameters = list(filter(None, parameters))
        return parameters
    except:

        return None

def getPrice(page, css_class):
    try:
        price = pages.data.getTag(page, 'div', css_class).text
        price = price.replace(' ', '')
        price = price.replace(';', '')
        price = price.split('\n')
        price = list(filter(None, price))
        return float(price[1].replace('р.',''))
    except:
        return None

def parsePage(page):
    try:
        description = getDescription(page, 'description')
        imageUrl = getImageUrl(page, 'product-info')
        filename = imageUrl[imageUrl.rfind('/') + 1:]
        imageFilename = 'images/' + imageUrl[imageUrl.rfind('/') + 1:]
        filename = filename[:filename.rfind('.')]
        pages.image.saveImage(imageUrl, imageFilename)
        parameters = getParameters(description)
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
        price = getPrice(page, 'price')
        json = ('[{"artikul":"' + artikul +
                '", "model":"' + model +
                '", "manufacturer":"' + manufacturer +
                '", "image":"' + imageFilename +
                '", "price":"' + str(price) +
                '", "link":"' + imageUrl + '"}]')

        pages.image.saveFile(json, 'json/' + filename + '.json', "w")
        return (json)
    except:
        return None

if not os.path.exists('images'):
    os.makedirs('images')
if not os.path.exists('json'):
    os.makedirs('json')

page = pages.data.getPage(URL)

links = pages.data.getChildUrls(page)
linksCategories = []
linksGoods = []
for link in links:
    if link.find(DOMEN) >= 0 and link.find('?') < 0 and link != URL:
        if not link in down:
            childPage = pages.data.getPage(link)
            if pages.data.isPageMatched(childPage, 'div', 'category-info'):
                linksCategories.append(link)
                childPageLinks = pages.data.getChildUrls(childPage)
                for childLink in childPageLinks:
                    if childLink.find(DOMEN) >= 0 and childLink.find('?') < 0 and childLink != URL and not childLink in linksGoods:
                        linksGoods.append(childLink)
            else:
                if not pages.data.isPageMatched(childPage, 'div', 'product-info'):
                    down.append(link)

for link in down:
    if link in linksGoods:
        list.remove(linksGoods, link)
for link in linksCategories:
    if link in linksGoods:
        list.remove(linksGoods, link)

goods = []
for link in linksGoods:
    page = pages.data.getPage(link)
    if pages.data.isPageMatched(page, 'div', 'product-info'):
        goods.append(parsePage(page))

pages.image.saveFile(str(goods), 'result.json', 'w')
for good in goods:
    good = json.loads(good)
    csv += (good[0]['artikul'] + ";"
            + good[0]['model'] + ";"
            + good[0]['manufacturer'] + ";"
            + good[0]['image'] + ";"
            + good[0]['price'] + ";"
            + good[0]['link'] + "\n")

try:
    pages.image.saveFile(csv, 'result.csv', 'w')
    if platform == 'win32' or platform == 'win64':
        df = pd.read_csv('result.csv', sep=';', encoding='windows-1251')
    else:
        df = pd.read_csv('result.csv', sep=';')
    df.to_excel('result.xlsx')
except:
    None
