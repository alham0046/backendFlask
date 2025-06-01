import requests
from bs4 import BeautifulSoup, SoupStrainer
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# headers2 = {
#     "cookie" : "_gid=GA1.2.975406441.1727196777; cf_clearance=GhoSONTw6bx0THe9YLyDY7vj16x5lfswSB_Jvqct6c4-1727199554-1.2.1.1-i5x2wHBejH5XMS2ASAyMSqBV.H2lT23h5BUWSAByy4Li_G_6YYhVo_aV7LDOwYLeDhUibvJhUGHA0tUE84RXY42dmEloQ_TYax29rcJjhjftjPBEiiQCZzJB.YlXfgZKnQHCB4uQN83vIaTiaRToE4Db1qel7nXK80w_UsJJe5J1KOfnvgYxOT9no.wjTJTZnEFyDSaYFlZCZzs8.99WDRX8SkWG4Whtle6xLIFKpe.3lDdkA59l5mD8o4G5JtHODt_8_LmB4i9rrjDbVJfPIz4K_L1i81mDvrQ7RUKuZIAh1yhRrbtMSwAYIoEOICWE4M3pM.hikXKjZU6AN1F5Q0KCgYoAHDJsjYduvgNv9s0.VNFVjOakBt7VxXEkXF18T.QkTFsBaI8oR8pSbctM1A; _ga=GA1.1.782194559.1726751383; _ga_TGHHGKF2QN=GS1.1.1727199556.4.1.1727199967.0.0.0",
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
#                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
# }

def sessionobj(VcloudUrl):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    })
    response = session.get(VcloudUrl)
    return response

def soupObject(url, strainer = "", isMovies = False, headers = headers, session = False, rawResponse = False, timeout = 10, checkLinkValidity = False, stream = False):
    print('the soupObject url is', url)
    if session:
        req = sessionobj(url)
    else:
        req = requests.get(url, headers=headers, timeout=timeout, stream=stream)
        if rawResponse == True or checkLinkValidity == True:
            return req
    if strainer:
        if isinstance(strainer, re.Pattern):
            strainer = SoupStrainer('div', attrs={'class':strainer})
        elif strainer.startswith('.'):
            strainer = SoupStrainer('div', attrs={'class':strainer.split('.')[1]})
            # return BeautifulSoup(req.content, 'html.parser', parse_only=strainer)
        elif strainer.startswith('#'):
            strainer = SoupStrainer('div', attrs={'id':strainer.split('#')[1]})
        return BeautifulSoup(req.content, 'html.parser', parse_only=strainer)
    else :
        return BeautifulSoup(req.content, 'html.parser')