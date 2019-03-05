import datetime
import json
import re
import scrapy
from locations.items import AddressItem


class CollegeStatsSpider(scrapy.Spider):
    download_delay = 0.5
    download_maxsize = 0
    name = "collegestats"
    allowed_domains = ["collegestats.org"]
    start_urls = (
        'https://collegestats.org/colleges/all/?pg=60',
    )

    def parse(self, response):
        schools = response.xpath('//tr[@class="school-listing-row"]')

        for school in schools:
            school_id = school.xpath('@data-school-id').extract_first()
            school_name = school.xpath('.//div[@class="name-location"]/p/text()').extract_first()

            if school_name is not None:
                base_url = 'https://collegestats.org/college'
                url = base_url + '/' + school_id + '-' + school_name.replace(' ', '-')

                request = scrapy.Request(url, callback=self.parse_school_details)

                # Collecting the college info on the college list page which is structured better
                # Carry this data as metadata to make it available to the subsequent school details parser
                request.meta['school_id'] = school.xpath('@data-school-id').extract_first()
                request.meta['name'] = school.xpath('.//div[@class="name-location"]/p/text()').extract_first()
                request.meta['street_address'] = school.xpath('.//meta[@itemprop="streetAddress"]/@content').extract_first()
                request.meta['city'] = school.xpath('.//meta[@itemprop="addressLocality"]/@content').extract_first()
                request.meta['state'] = school.xpath('.//meta[@itemprop="addressRegion"]/@content').extract_first()
                request.meta['postcode'] = school.xpath('.//meta[@itemprop="postalCode"]/@content').extract_first()

                yield request

            else:
                continue

        next_page_url = response.xpath('//ol[@class="pagination"]/li[position() = (last()-1)]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_school_details(self, elements):
        ref = re.search(r'.+/(.+)', elements.url).group(1)

        items = {
            'ref': ref,
            'school_id': elements.meta['school_id'],
            'name': elements.meta['name'],
            'street_address': elements.meta['street_address'],
            'city': elements.meta['city'],
            'state': elements.meta['state'],
            'postcode': elements.meta['postcode'],
            'website': elements.xpath('//section[@class="content school"]/button/a/@href').extract_first()
        }

        yield AddressItem(**items)
