import scrapy
import requests
from bs4 import BeautifulSoup as bs
import re

class SBD(scrapy.Spider):
    name = 'sbd'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
    urls = []

    def start_requests(self):
        sitemap = 'https://www.smartbusinessdirectory.co.uk/sitemap.xml'

        page = bs(requests.get(sitemap, headers=self.headers).text, 'html.parser')
        links = [link.text for link in page.find_all('loc', text=re.compile('.*/[a-z0-9\-]*\.html'))]

        for link in links:
            page = bs(requests.get(link, headers=self.headers).text, 'html.parser')
            
            self.urls.extend(['https://www.smartbusinessdirectory.co.uk' + url.get('href') for url in page.select('div.navtop a')])
            print(self.urls)

        print(self.urls)
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)


    def parse(self, response):
        title = response.css('div.navtop::text').extract_first()

        if not title:
            return

        contact = response.css('div[class="article white tleft"] ul li:nth-child(1)::text').extract_first()
        address = response.css('div[class="article white tleft"] ul li:nth-child(2)::text').extract_first()
        website = response.css('div[class="article white tleft"] ul li:nth-child(3) a::text').extract_first()
        other = response.css('div[class="article white tleft"] ul li:nth-child(4) a::text').extract()
        description = response.css('div[class="article white tleft"] ul li:nth-child(5)::text').extract_first()
        listing = response.css('div[class="article white tleft"] ul li:nth-child(6) a::text').extract()
        business_areas = response.css('div[class="article white tleft"] ul li:nth-child(7) a::text').extract()

        data = {
            'title': title,
            'contact': contact,
            'address': address,
            'website': website,
            'other_pages': other,
            'description': description,
            'listings': listing,
            'business_areas': business_areas,
            'source_url': response.url
        }

        self.log(data)

        yield data