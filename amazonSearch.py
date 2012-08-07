import urllib2
from xmltodict import xmltodict
from amazon.api import AmazonAPI

class Amazon:

    amazonId = 'AKIAIXBPPRN2LXDFNBDQ'
    amazonAssoc = 'listify-20'
    secretKey = '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'
    category = 'All';
    query = 'starwars'
    url = 'http://ecs.amazonaws.com/onca/xml?Service='\
    + 'AWSECommerceService&IdType=ASIN&ResponseGroup=Large&SearchIndex='\
    + category\
    + '&Operation=ItemSearch&Keywords='\
    + query\
    + '&AWSAccessKeyId='\
    + amazonId\
    + '&AssociateTag='\
    + amazonAssoc
    # print url
    amazonUrl = 'http://ecs.amazonaws.com/onca/xml?AWSAccessKeyId='\
    + 'AKIAIXBPPRN2LXDFNBDQ&AssociateTag=listify-20&IdType=ASIN&Keywords='\
    + query\
    + '&Operation=ItemSearch&ResponseGroup=Large&SearchIndex='\
    + category\
    + '&Service=AWSECommerceService&Timestamp=2012-08-05T15%3A49%3A56.000Z'\
    + '&Signature=7BRFKgK3Ro4XjtrzkRG712mq0OFRkafcVhox4%2BQ%2BK2k%3D'
# print amazonUrl
    amazonUrl = 'http://ecs.amazonaws.com/onca/xml?AWSAccessKeyId=AKIAIXBPPRN2LXDFNBDQ&AssociateTag=listify-20&IdType=ASIN&Keywords=vynil&Operation=ItemSearch&ResponseGroup=Large&SearchIndex=Music&Service=AWSECommerceService&Timestamp=2012-08-05T16%3A52%3A12.000Z&Signature=KU9rOWQB%2F2HbgNp2TGActQ2InQtdl9jItbGtNaxR0s0%3D'

    def fetch(self):
        self.api = AmazonAPI(self.amazonId, self.secretKey, self.amazonAssoc)
        self.products = self.api.search(Keywords='My Bloody Valentine', SearchIndex='Music')

        # response = self.api.item_search('Music', Artist='My Bloody Valentine')

        # self.products = response
        # req = urllib2.Request(self.amazonUrl)
        # response = urllib2.urlopen(req)
        # the_page = response.read()
        # self.results = xmltodict(the_page)
# print results['Items'][0]['Item'][0]['Title']

    def getArtist(self, index):
        return self.results['Items'][0]['Item'][index]['ItemAttributes'][0]['Artist'][0]


    def getTitle(self, index):
        return self.results['Items'][0]['Item'][index]['ItemAttributes'][0]['Title'][0]
