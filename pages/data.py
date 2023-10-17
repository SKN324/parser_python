from bs4 import BeautifulSoup as bs
import requests

def getPage(url):
    try:
        session = requests.session()
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        html = session.get(url, headers = headers)

        return bs(html.text, 'html5lib')
    except:
        return None

def getChildUrls(page):
    try:
        links = []
        for tag in page.find_all('a'):
            links.append(str(tag.attrs.get('href')))

        return links
    except:

        return None

def isPageMatched(page, tag, css_class):
    try:
        result = page.find(tag, css_class)
    except:
        result = None

    if result and result != '':

        return True
    else:

        return False

def getTag(page, tag, css_class):
    try:

        return page.find(tag, css_class)
    except:

        return None
