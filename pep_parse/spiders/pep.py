import scrapy

from pep_parse.items import PepParseItem
from pep_parse.utils import parse_status
from pep_parse.constants import NAME, ALLOWED_DOMAINS, START_URLS


class PepSpider(scrapy.Spider):
    name = NAME
    allowe_domains = ALLOWED_DOMAINS
    start_urls = START_URLS

    def parse(self, response):
        peps = response.css('section#numerical-index a::attr(href)')
        for pep_link in peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_detail = response.css('h1.page-title::text').get()
        data = {
            'number': int(pep_detail.split()[1].strip()),
            'name': pep_detail.strip(),
            'status': parse_status(response),
        }
        yield PepParseItem(data)
