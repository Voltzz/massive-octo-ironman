from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from sarscrape.items import SarscrapeItem

class SardatabaseSpider(CrawlSpider):
    name = 'sardatabase'
    allowed_domains = ['sardatabase.com']
    start_urls = ['http://www.sardatabase.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/(w|w-w)'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = SarscrapeItem()
	i['brand'] = hxs.select('//h1/text()').extract()
	i['device'] = hxs.select('//table/tr/td/text()').extract()
        return i
