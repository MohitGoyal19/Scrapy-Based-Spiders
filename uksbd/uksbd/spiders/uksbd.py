import scrapy
import requests
from bs4 import BeautifulSoup as bs
import json

class UKSBD(scrapy.Spider):
    name = 'uksbd'
    urls = []

    def get_links(self, url):
        page_source = requests.get(url).text

        page_source = bs(page_source, 'html.parser')

        links = [link.get('href') for link in page_source.select('.nobordercontainer div div a:nth-child(7)')]
        if not links:
            links = [link.get('href') for link in page_source.select('a:nth-child(20)')]
        if not links:
            links = [link.get('href') for link in page_source.select('br~ div div a')]
        if not links:
            links = [link.get('href') for link in page_source.select('br+ div div a')]

        self.urls.extend(links)
        print('Urls: ', len(self.urls))     

    
    def start_requests(self):
        county_url = 'https://www.uksmallbusinessdirectory.co.uk/cat-in-county-'

        for i in range(97, 123):
            url = county_url+chr(i)
            
            page_source = requests.get(url).text

            page_source = bs(page_source, 'html.parser')

            links = [link.get('href') for link in page_source.select('ol a')]

            for link in links:
                self.get_links(link)

        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.css('script[type="application/ld+json"]::text').extract_first()

        if not data:
            return

        data = json.loads(data)
        address = data['address']['streetAddress'] + ', ' + data['address']['addressLocality'] + ', ' + data['address']['addressRegion']
        postal_code = data['address']['postalCode'].upper()
        ref_no = response.url.split('/')[-2]

        yield{
            'business_type': data['@type'],
            'name': data['name'],
            'description': data['description'],
            'address': address,
            'post_code': postal_code,
            'contact': data['telephone'],
            'source_url': response.url,
            'reference_no': ref_no
        }
        