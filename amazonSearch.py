from xml.dom.minidom import parse, parseString
from settings import amazon_id, amazon_assoc, secret_key
import bottlenose


class Amazon:

    amazonId = amazon_id
    amazonAssoc = amazon_assoc
    secretKey = secret_key

    def __init__(self):
        self.albums = []

    def fetch(self, artist):
        self.albums = []
        self.api = bottlenose.Amazon(self.amazonId, self.secretKey, self.amazonAssoc)
        self.apiEs = bottlenose.Amazon(self.amazonId, self.secretKey, self.amazonAssoc, None, None, '2011-08-01','ES')
        self.apiUK = bottlenose.Amazon(self.amazonId, self.secretKey, self.amazonAssoc, None, None, '2011-08-01','UK')

        self.getProducts(self.api, 'com', artist)
        self.getProducts(self.apiEs, 'es', artist)
        self.getProducts(self.apiUK, 'co.uk', artist)

    def getProducts(self, api, source, artist):
        products = api.ItemSearch(SearchIndex='Music', Artist=artist, ResponseGroup="ItemAttributes,Images,Offers", MerchantId="Amazon")
        dom = parseString(products)
        self.addAlbums(dom, source)

        item_page = 0
        i = 1

        while dom.getElementsByTagName('TotalPages').length > 0 and \
        int(dom.getElementsByTagName('TotalPages')[0].firstChild.nodeValue) > (item_page + 1) and \
        i < 10:
            products = api.ItemSearch(SearchIndex='Music', Artist=artist, ItemPage=i, ResponseGroup="ItemAttributes,Images,Offers", MerchantId="Amazon")
            i = i + 1
            dom = parseString(products)
            self.addAlbums(dom, source)
            item_page = int(dom.getElementsByTagName('ItemPage')[0].firstChild.nodeValue)


    def addAlbums(self, dom, source):
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
                item = ''
                # print 'dom '+source+': '+str(i) + ' of ' + str(batch_size)
                try:
                    item = self.getItem(dom, i)
                    if item['Binding'] == 'Vinyl' or item['Binding'] == 'Disco de vinilo':
                        album['artist'] = item['Artist']
                        album['title'] = item['Title']
                        album['ASIN'] = item['ASIN']
                        album['URL'] = item['URL']
                        album['price'] = item['Price']
                        try:
                            album['thumbnail'] = item['Image_S']
                        except:
                            album['thumbnail'] = ''
                        try:
                            album['image'] = item['Image_M']
                        except:
                            album['image'] = ''
                        album['availability'] = item['Availability']
                        album['currency'] = item['CurrencyCode']
                        album['source'] = source
                        self.albums.append(album)
                except:
                    print 'Not enought data to fetch this album' # this shouldn't ever ever happen
                    # print item


    def getItem(self, dom, index):
        debug = 0
        try:
            item = dom.getElementsByTagName("Item")[index]
            itemData = {}
            itemData['Artist'] = item.getElementsByTagName("Artist")[0].firstChild.nodeValue
            debug = 1
            itemData['Title'] = item.getElementsByTagName("Title")[0].firstChild.nodeValue
            debug = 2
            itemData['ASIN'] = item.getElementsByTagName("ASIN")[0].firstChild.nodeValue
            debug = 3
            itemData['URL'] = item.getElementsByTagName("DetailPageURL")[0].firstChild.nodeValue
            debug = 4
            itemData['Binding'] = item.getElementsByTagName("Binding")[0].firstChild.nodeValue
            debug = 5
            itemData['Price'] = item.getElementsByTagName("OfferListing")[0].\
            getElementsByTagName("Amount")[0].firstChild.nodeValue
            debug = 6
            itemData['CurrencyCode'] = item.getElementsByTagName("OfferListing")[0].\
            getElementsByTagName("CurrencyCode")[0].firstChild.nodeValue
            debug = 7
            itemData['Availability'] = item.getElementsByTagName("AvailabilityType")[0].firstChild.nodeValue
            debug = 8
            try:
                itemData['Image_S'] = item.getElementsByTagName("SmallImage")[0].\
                getElementsByTagName('URL')[0].firstChild.nodeValue
                debug = 9
            except:
                itemData['Image_S'] = None
                debug = 10
            try:
                itemData['Image_M'] = item.getElementsByTagName("MediumImage")[0].\
                getElementsByTagName('URL')[0].firstChild.nodeValue
                debug = 11
            except:
                itemData['Image_M'] = None
                debug = 12
            # itemData['Image'] = item.getElementsByTagName("Image")[0].firstChild.nodeValue
        except:
            print debug
        return itemData

