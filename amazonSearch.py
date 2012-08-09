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

        self.api = bottlenose.Amazon(self.amazonId, self.secretKey, self.amazonAssoc)
        self.products = self.api.ItemSearch(SearchIndex='Music', Keywords='vinyl', Artist=artist, ResponseGroup="ItemAttributes,Images", MerchantId="Amazon")
        dom = parseString(self.products)
        self.addAlbums(dom)
        item_page = 0

        i = 1
        while dom.getElementsByTagName('TotalPages').length > 0 and \
        int(dom.getElementsByTagName('TotalPages')[0].firstChild.nodeValue) > (item_page + 1) and \
        i < 10:
            self.products = self.api.ItemSearch(SearchIndex='Music', Keywords='vinyl', Artist=artist, ItemPage=i, ResponseGroup="ItemAttributes,Images", MerchantId="Amazon")
            i = i + 1
            dom = parseString(self.products)
            self.addAlbums(dom)
            item_page = int(dom.getElementsByTagName('ItemPage')[0].firstChild.nodeValue)

    def addAlbums(self, dom):
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
                    item = self.getItem(dom, i)
                    if item['Binding'] == 'Vinyl':
                        album['artist'] = item['Artist']
                        album['title'] = item['Title']
                        album['ASIN'] = item['ASIN']
                        album['URL'] = item['URL']
                        album['price'] = item['Price']
                        album['thumbnail'] = item['Image_S']
                        album['image'] = item['Image_M']
                        self.albums.append(album)
                except:
                    print 'Not enought data to fetch this album' # this shouldn't ever ever happen


    def getItem(self, dom, index):
        item = dom.getElementsByTagName("Item")[index]
        itemData = {}
        itemData['Artist'] = item.getElementsByTagName("Artist")[0].firstChild.nodeValue
        itemData['Title'] = item.getElementsByTagName("Title")[0].firstChild.nodeValue
        itemData['ASIN'] = item.getElementsByTagName("ASIN")[0].firstChild.nodeValue
        itemData['URL'] = item.getElementsByTagName("DetailPageURL")[0].firstChild.nodeValue
        itemData['Binding'] = item.getElementsByTagName("Binding")[0].firstChild.nodeValue
        itemData['Price'] = item.getElementsByTagName("ListPrice")[0].\
        getElementsByTagName("Amount")[0].firstChild.nodeValue
        itemData['Image_S'] = item.getElementsByTagName("SmallImage")[0].\
        getElementsByTagName('URL')[0].firstChild.nodeValue
        itemData['Image_M'] = item.getElementsByTagName("MediumImage")[0].\
        getElementsByTagName('URL')[0].firstChild.nodeValue
        # itemData['Image'] = item.getElementsByTagName("Image")[0].firstChild.nodeValue
        return itemData

