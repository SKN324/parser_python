import requests

def saveImage(imageUrl, filename):
    try:
        session = requests.session()
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        data = session.get(imageUrl, headers=headers)
        saveFile(data.content, filename, "wb")

    except:

        return

def saveFile(content, filename, format):
    try:
        file = open(filename, format)
        file.write(content)
        file.close()
    except:

        return