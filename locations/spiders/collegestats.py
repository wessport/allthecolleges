import datetime
import json
import re
import scrapy
from locations.items import AddressItem

class CollegeStatsSpider(scrapy.Spider):
    download_delay = 0.05
    name = "collegestats"
    allowed_domains = ["collegestats.org"]
    start_urls = (
        'https://collegestats.org/colleges/tennessee/',
    )

    def parse(self, response):
        ref = re.search(r'.+/(.+)?/', response.url).group(1)
        schools = response.xpath('//tr[@class="school-listing-row"]')

        for school in schools:
            properties =  {
                'ref': ref,
                'school_id': school.xpath('@data-school-id').extract_first(),
                'name': school.xpath('.//div[@class="name-location"]/p/text()').extract_first(),
                'street_address': school.xpath('.//meta[@itemprop="streetAddress"]/@content').extract_first(),
                'city': school.xpath('.//meta[@itemprop="addressLocality"]/@content').extract_first(),
                'state': school.xpath('.//meta[@itemprop="addressRegion"]/@content').extract_first(),
                'postcode': school.xpath('.//meta[@itemprop="postalCode"]/@content').extract_first()
                }

            yield AddressItem(**properties)

        next_page_url = response.xpath('//ol[@class="pagination"]/li[position() = (last()-1)]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
