from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from craigscrape.items import CraigscrapeItem

class CraigslistSpider(CrawlSpider):
    name = 'craigslist'
    allowed_domains = ['toronto.en.craigslist.ca']
    start_urls = ['http://toronto.en.craigslist.ca/moa/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/tor/mob/\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = CraigscrapeItem()
	i['title'] = hxs.select("//h2/text()").extract()
	i['desc'] = hxs.select("//section[@id='postingbody']/text()").extract()
        return i
