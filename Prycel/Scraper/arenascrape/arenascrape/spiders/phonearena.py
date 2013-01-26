from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from arenascrape.items import ArenascrapeItem

class PhonearenaSpider(CrawlSpider):
    name = 'phonearena'
    allowed_domains = ['phonearena.com']
    start_urls = ['http://www.phonearena.com/phones/manufacturers/']

    rules = (
        Rule(SgmlLinkExtractor(allow=[start_urls[0] + r'(\w|\w-\w)'], deny=[start_urls[0] + r'(\w|\w-\w)/'], restrict_xpaths=(["//div[@class=\"s_pager s_pager_s_size_2 s_p_20_0\"]", "//div[@id=\"brands\"]"])), callback='parse_item', follow=True),
	Rule(SgmlLinkExtractor(allow=[start_urls[0] + r'(\w|\w-\w)/page/[0-9]+'], restrict_xpaths=("//div[@class=\"s_pager s_pager_s_size_2 s_p_20_0\"]")), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = ArenascrapeItem()
	i['brand'] = hxs.select('//h1/text()').extract()
	i['device'] = hxs.select('//div[@class="s_listing"]/h3/text()').extract()
        return i
