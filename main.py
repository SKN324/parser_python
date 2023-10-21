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

# linksCategories = ['http://novotechnic.ru/watering/', 'http://novotechnic.ru/watering/watering_complects/', 'http://novotechnic.ru/watering/watering_modules/', 'http://novotechnic.ru/watering/watering_parts/']
# down = ['http://novotechnic.ru/login/', 'http://novotechnic.ru/create-account/', 'http://novotechnic.ru/wishlist/', 'http://novotechnic.ru/cart/', 'http://novotechnic.ru/checkout/', 'http://novotechnic.ru/contacts.html', 'http://novotechnic.ru/delivery.html', 'http://novotechnic.ru/safety.html', 'http://novotechnic.ru/forgot-password/', 'http://novotechnic.ru/my-account/', 'http://novotechnic.ru/address-book/', 'http://novotechnic.ru/order-history/', 'http://novotechnic.ru/downloads/', 'http://novotechnic.ru/returns/', 'http://novotechnic.ru/transactions/', 'http://novotechnic.ru/newsletter/', 'http://novotechnic.ru/offerta.html', 'http://novotechnic.ru/contact-us/', 'http://novotechnic.ru/sitemap/', 'http://novotechnic.ru/brands/', 'http://novotechnic.ru/vouchers/', 'http://novotechnic.ru/affiliates/', 'http://novotechnic.ru/specials/']
# linksGoods = ['http://novotechnic.ru/login/', 'http://novotechnic.ru/create-account/', 'http://novotechnic.ru/wishlist/', 'http://novotechnic.ru/cart/', 'http://novotechnic.ru/checkout/', 'http://novotechnic.ru/watering/', 'http://novotechnic.ru/watering/watering_complects/', 'http://novotechnic.ru/watering/watering_modules/', 'http://novotechnic.ru/watering/watering_parts/', 'http://novotechnic.ru/contacts.html', 'http://novotechnic.ru/delivery.html', 'http://novotechnic.ru/safety.html', 'http://novotechnic.ru/compare-products/', 'http://novotechnic.ru/watering/kit_t26-0.html', 'http://novotechnic.ru/watering/kit_t36-0.html', 'http://novotechnic.ru/watering/kit_t36-90.html', 'http://novotechnic.ru/watering/kit_t36-0k.html', 'http://novotechnic.ru/watering/kit_t36-90k.html', 'http://novotechnic.ru/watering/kit_t36-0b.html', 'http://novotechnic.ru/watering/kit_t36-90b.html', 'http://novotechnic.ru/watering/watering_modules/truba_002tr6-90.html', 'http://novotechnic.ru/watering/truba_002tr6-0.html', 'http://novotechnic.ru/watering/truba_002tr6-180.html', 'http://novotechnic.ru/watering/truba_002tr8-90.html', 'http://novotechnic.ru/watering/truba_002tr8-0.html', 'http://novotechnic.ru/watering/truba_002tr8-180.html', 'http://novotechnic.ru/watering/opora_003os05.html', 'http://novotechnic.ru/watering/opora_003os05k.html', 'http://novotechnic.ru/watering/opora_003om05.html', 'http://novotechnic.ru/watering/opora_003oe05.html', 'http://novotechnic.ru/watering/watering_modules/kol_001km110.html', 'http://novotechnic.ru/watering/troynic_001tm5.html', 'http://novotechnic.ru/watering/krest_001kr5.html', 'http://novotechnic.ru/watering/truba_pvc_001pvc1.html', 'http://novotechnic.ru/watering/truba_pvc_001pvc100.html', 'http://novotechnic.ru/watering/kran_001ks12ff.html', 'http://novotechnic.ru/watering/watering_parts/kran_001ks12fm.html', 'http://novotechnic.ru/watering/watering_parts/zaglushka_001z12f.html', 'http://novotechnic.ru/offerta.html', 'http://novotechnic.ru/contact-us/', 'http://novotechnic.ru/sitemap/', 'http://novotechnic.ru/brands/', 'http://novotechnic.ru/vouchers/', 'http://novotechnic.ru/affiliates/', 'http://novotechnic.ru/specials/', 'http://novotechnic.ru/my-account/', 'http://novotechnic.ru/order-history/', 'http://novotechnic.ru/newsletter/', 'http://novotechnic.ru/watering/truba_pnd_001pnd1.html', 'http://novotechnic.ru/watering/watering_modules/truba_pnd_001pnd100.html', 'http://novotechnic.ru/watering/watering_parts/filtr_001f12ff.html', 'http://novotechnic.ru/watering/watering_modules/prokladka_001p12.html', 'http://novotechnic.ru/watering/watering_parts/zaglushka_001z12m.html', 'http://novotechnic.ru/watering/watering_parts/mufta_001m12ff.html', 'http://novotechnic.ru/watering/watering_parts/mufta_001m12mm.html', 'http://novotechnic.ru/watering/watering_parts/ugolok_001u12ff.html', 'http://novotechnic.ru/watering/watering_parts/ugolok_001u12fm.html', 'http://novotechnic.ru/watering/watering_parts/mufta_001cm12fx25.html', 'http://novotechnic.ru/watering/watering_parts/mufta_001cm12mx25.html', 'http://novotechnic.ru/watering/watering_parts/mufta_001cm2500.html', 'http://novotechnic.ru/watering/watering_parts/otvod_001cm2590.html', 'http://novotechnic.ru/watering/watering_parts/troynic_001ct25.html']

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

# goods = ['[{"artikul":"T26-0", "model":"T26-0", "manufacturer":"Novotechnic", "image":"images/kit_M36-180_500-1000x1000.jpg", "price":"1950.0", "link":"http://novotechnic.ru/image/cache/data/catalog/kits/kit_M36-180_500-1000x1000.jpg"}]', '[{"artikul":"T36-0", "model":"T36-0", "manufacturer":"Novotechnic", "image":"images/kit_M36-180_500-1000x1000.jpg", "price":"2750.0", "link":"http://novotechnic.ru/image/cache/data/catalog/kits/kit_M36-180_500-1000x1000.jpg"}]', '[{"artikul":"T36-90", "model":"T36-90", "manufacturer":"Novotechnic", "image":"images/kit_M36-180_500-1000x1000.jpg", "price":"2750.0", "link":"http://novotechnic.ru/image/cache/data/catalog/kits/kit_M36-180_500-1000x1000.jpg"}]', '[{"artikul":"T36-0k", "model":"T36-0k", "manufacturer":"Novotechnic", "image":"images/kit_M36-0k_500-1000x1000.jpg", "price":"2950.0", "link":"http://novotechnic.ru/image/cache/data/catalog/kits/kit_M36-0k_500-1000x1000.jpg"}]', '[{"artikul":"T36-90k", "model":"T36-90k", "manufacturer":"Novotechnic", "image":"images/kit_M36-0k_500-1000x1000.jpg", "price":"2950.0", "link":"http://novotechnic.ru/image/cache/data/catalog/kits/kit_M36-0k_500-1000x1000.jpg"}]', '[{"artikul":"T36-0b", "model":"T36-0b", "manufacturer":"Novotechnic", "image":"images/kit_M36-0b_500-1000x1000.jpg", "price":"4450.0", "link":"http://novotechnic.ru/image/cache/data/catalog/kits/kit_M36-0b_500-1000x1000.jpg"}]', '[{"artikul":"T36-90b", "model":"T36-90b", "manufacturer":"Novotechnic", "image":"images/kit_M36-0b_500-1000x1000.jpg", "price":"4450.0", "link":"http://novotechnic.ru/image/cache/data/catalog/kits/kit_M36-0b_500-1000x1000.jpg"}]', '[{"artikul":"002TR6-90", "model":"002TR6-90", "manufacturer":"Novotechnic", "image":"images/trassa_500-1000x1000.jpg", "price":"465.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/trassa_500-1000x1000.jpg"}]', '[{"artikul":"002TR6-0", "model":"002TR6-0", "manufacturer":"Novotechnic", "image":"images/trassa_500_0-1000x1000.jpg", "price":"465.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/trassa_500_0-1000x1000.jpg"}]', '[{"artikul":"002TR6-180", "model":"002TR6-180", "manufacturer":"Novotechnic", "image":"images/trassa_500_180-1000x1000.jpg", "price":"465.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/trassa_500_180-1000x1000.jpg"}]', '[{"artikul":"002TR8-90", "model":"002TR8-90", "manufacturer":"Novotechnic", "image":"images/trassa_500-1000x1000.jpg", "price":"575.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/trassa_500-1000x1000.jpg"}]', '[{"artikul":"002TR8-0", "model":"002TR8-0", "manufacturer":"Novotechnic", "image":"images/trassa_500_0-1000x1000.jpg", "price":"575.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/trassa_500_0-1000x1000.jpg"}]', '[{"artikul":"002TR8-180", "model":"002TR8-180", "manufacturer":"Novotechnic", "image":"images/trassa_500_180-1000x1000.jpg", "price":"575.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/trassa_500_180-1000x1000.jpg"}]', '[{"artikul":"003OS05", "model":"003OS05", "manufacturer":"Novotechnic", "image":"images/opora_start_500-1000x1000.jpg", "price":"330.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/opora_start_500-1000x1000.jpg"}]', '[{"artikul":"003OS05K", "model":"003OS05K", "manufacturer":"Novotechnic", "image":"images/opora_start_500k-1000x1000.jpg", "price":"570.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/opora_start_500k-1000x1000.jpg"}]', '[{"artikul":"003OM05", "model":"003OM05", "manufacturer":"Novotechnic", "image":"images/opora_mid_500-1000x1000.jpg", "price":"290.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/opora_mid_500-1000x1000.jpg"}]', '[{"artikul":"003OE05", "model":"003OE05", "manufacturer":"Novotechnic", "image":"images/opora_end_500-1000x1000.jpg", "price":"290.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/opora_end_500-1000x1000.jpg"}]', '[{"artikul":"001KM110", "model":"001KM110", "manufacturer":"", "image":"images/kol_500-1000x1000.jpg", "price":"12.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/kol_500-1000x1000.jpg"}]', '[{"artikul":"001TM5", "model":"001TM5", "manufacturer":"", "image":"images/troynicm_500-1000x1000.jpg", "price":"10.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/troynicm_500-1000x1000.jpg"}]', '[{"artikul":"001KR5", "model":"001KR5", "manufacturer":"", "image":"images/krest_500-1000x1000.jpg", "price":"20.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/krest_500-1000x1000.jpg"}]', '[{"artikul":"001PVC1", "model":"001PVC1", "manufacturer":"", "image":"images/pvh_otrez_500-1000x1000.jpg", "price":"17.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/pvh_otrez_500-1000x1000.jpg"}]', '[{"artikul":"001PVC100", "model":"001PVC100", "manufacturer":"", "image":"images/pvh_buhta_500-1000x1000.jpg", "price":"1400.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/pvh_buhta_500-1000x1000.jpg"}]', '[{"artikul":"001KS12FF", "model":"001KS12FF", "manufacturer":"SAS", "image":"images/kranff_500_1-1000x1000.jpg", "price":"306.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/kranff_500_1-1000x1000.jpg"}]', '[{"artikul":"001KS12FM", "model":"001KS12FM", "manufacturer":"SAS", "image":"images/kran_500-1000x1000.jpg", "price":"306.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/kran_500-1000x1000.jpg"}]', '[{"artikul":"001Z12F", "model":"001Z12F", "manufacturer":"Santrade", "image":"images/zagl12m_500-1000x1000.jpg", "price":"40.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/zagl12m_500-1000x1000.jpg"}]', '[{"artikul":"001PND1", "model":"001PND1", "manufacturer":"Политэк", "image":"images/pnd_500-1000x1000.jpg", "price":"50.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/pnd_500-1000x1000.jpg"}]', '[{"artikul":"001PND100", "model":"001PND100", "manufacturer":"Политэк", "image":"images/pnd_500-1000x1000.jpg", "price":"3900.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/pnd_500-1000x1000.jpg"}]', '[{"artikul":"001F12FF", "model":"001F12FF", "manufacturer":"Santrade", "image":"images/filtr_500-1000x1000.jpg", "price":"170.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/filtr_500-1000x1000.jpg"}]', '[{"artikul":"001P12", "model":"001P12", "manufacturer":"", "image":"images/prokladka_zagl12m_500-1000x1000.jpg", "price":"1.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/prokladka_zagl12m_500-1000x1000.jpg"}]', '[{"artikul":"001Z12M", "model":"001Z12M", "manufacturer":"Santrade", "image":"images/zagl12p_500-1000x1000.jpg", "price":"40.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/zagl12p_500-1000x1000.jpg"}]', '[{"artikul":"001M12FF", "model":"001M12FF", "manufacturer":"Santrade", "image":"images/nippelm_500-1000x1000.jpg", "price":"85.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/nippelm_500-1000x1000.jpg"}]', '[{"artikul":"001M12MM", "model":"001M12MM", "manufacturer":"Santrade", "image":"images/nippel_500-1000x1000.jpg", "price":"49.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/nippel_500-1000x1000.jpg"}]', '[{"artikul":"001U12FF", "model":"001U12FF", "manufacturer":"Santrade", "image":"images/uglff_500-1000x1000.jpg", "price":"143.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/uglff_500-1000x1000.jpg"}]', '[{"artikul":"001U12FM", "model":"001U12FM", "manufacturer":"Santrade", "image":"images/uglfm_500-1000x1000.jpg", "price":"150.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/uglfm_500-1000x1000.jpg"}]', '[{"artikul":"001CM12FX25", "model":"001CM12FX25", "manufacturer":"Политэк", "image":"images/mufta12m_500-1000x1000.jpg", "price":"36.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/mufta12m_500-1000x1000.jpg"}]', '[{"artikul":"001CM12MX25", "model":"001CM12MX25", "manufacturer":"Политэк", "image":"images/mufta12p_500-1000x1000.jpg", "price":"36.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/mufta12p_500-1000x1000.jpg"}]', '[{"artikul":"001CM2500", "model":"001CM2500", "manufacturer":"Политэк", "image":"images/mufta_500-1000x1000.jpg", "price":"62.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/mufta_500-1000x1000.jpg"}]', '[{"artikul":"001CM2590", "model":"001CM2590", "manufacturer":"Политэк", "image":"images/otvod_500-1000x1000.jpg", "price":"45.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/otvod_500-1000x1000.jpg"}]', '[{"artikul":"001CT25", "model":"001CT25", "manufacturer":"Политэк", "image":"images/troynic_500-1000x1000.jpg", "price":"57.0", "link":"http://novotechnic.ru/image/cache/data/catalog/goods/troynic_500-1000x1000.jpg"}]']

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
