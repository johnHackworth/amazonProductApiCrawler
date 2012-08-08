import urllib2
from xmltodict import xmltodict
from amazonproduct import API
from xml.dom.minidom import parse, parseString
import bottlenose

class Amazon:

    amazonId = 'AKIAIXBPPRN2LXDFNBDQ'
    amazonAssoc = 'listify-20'
    secretKey = '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'

    def __init__(self):
        self.albums = []

    def fetch(self, artist):

        self.api = bottlenose.Amazon(self.amazonId, self.secretKey, self.amazonAssoc)
        self.products = self.api.ItemSearch(SearchIndex='Music', Keywords='vinyl', Artist=artist)
        self.offers = self.api.ItemSearch(SearchIndex='Music', Keywords='vinyl', Artist=artist, ResponseGroup="OfferFull")
        dom = parseString(self.products)
        i = 1
        offerDom = parseString(self.offers)
        prices = self.getPrices(offerDom)
        self.addAlbums(dom, prices)
        item_page = 0

        while dom.getElementsByTagName('TotalPages').length > 0 and \
        int(dom.getElementsByTagName('TotalPages')[0].firstChild.nodeValue) > (item_page + 1) and \
        i < 10:
            self.products = self.api.ItemSearch(SearchIndex='Music', Keywords='vinyl', Artist=artist, ItemPage=i)
            self.offers = self.api.ItemSearch(SearchIndex='Music', Keywords='vinyl', Artist=artist, ItemPage=i, ResponseGroup="OfferFull")
            i = i + 1
            dom = parseString(self.products)
            offerDom = parseString(self.offers)
            prices = self.getPrices(offerDom)
            self.addAlbums(dom, prices)
            item_page = int(dom.getElementsByTagName('ItemPage')[0].firstChild.nodeValue)

    def addAlbums(self, dom, prices):
        total_results = dom.getElementsByTagName("TotalResults")[0].firstChild.nodeValue
        if int(total_results) > 0:
            total_pages = dom.getElementsByTagName("TotalPages")[0].firstChild.nodeValue
            item_page = 0
            if dom.getElementsByTagName("ItemPage").length > 0:
                item_page = dom.getElementsByTagName("ItemPage")[0].firstChild.nodeValue
            batch_size = 10
            if int(total_pages) == int(item_page) + 1:
                batch_size = int(total_results) % 10

            for i in range(batch_size):
                album = {}
                try:
                    album['artist'] = self.getArtist(dom, i)
                    album['album'] = self.getTitle(dom, i)
                    album['ASIN'] = self.getASIN(dom, i)
                    album['URL'] = self.getURL(dom, i)
                    if album['ASIN'] in prices:
                        album['price'] = prices[album['ASIN']]
                    self.albums.append(album)
                except:
                    print 'error fetching an album' # this shouldn't ever ever happen

    def getArtist(self, dom, index):
        return dom.getElementsByTagName("Artist")[index].firstChild.nodeValue

    def getTitle(self, dom, index):
        return dom.getElementsByTagName("Title")[index].firstChild.nodeValue

    def getASIN(self, dom, index):
        return dom.getElementsByTagName("ASIN")[index].firstChild.nodeValue

    def getURL(self, dom, index):
        return dom.getElementsByTagName("URL")[index].firstChild.nodeValue


    def getPrices(self, dom):
        albums = dom.getElementsByTagName('ASIN')
        albumPrice = {}
        for album in albums:
            asin = album.firstChild.nodeValue
            prices = album.parentNode.getElementsByTagName('LowestNewPrice')
            if prices.length > 0:
                price = prices[0].getElementsByTagName('Amount')[0].firstChild.nodeValue
                albumPrice[asin] = price

        return albumPrice

