import requests
import scrapy
from bs4 import BeautifulSoup as bs
import json

class blacktown(scrapy.Spider):
    name = 'blacktown'
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}


    def start_requests(self):
        url = 'https://www.whereis.com/singleSearch?query={}&bounds=-33.71500751422707%2C150.7766572625%2C-33.82388669829108%2C151.04032913750004&paginationRequestPage={}&firstvisit=true'
        #businesses = ['Accountant', 'Doctor', 'Estate', 'Hair', 'Repair']
        businesses = []
        business_url = 'https://www.whereis.com/seo/alphaCategories/NSW/Blacktown/index-{}?postcode=2148'

        for i in range(97, 123): #lowercase alphabets
            page = bs(requests.get(business_url.format(chr(i))).text, 'html.parser')
            categories = page.find('div', {'id': 'alphabetic-categories'}).find_all('h3')
            for business in categories:
                businesses.append(business.text.replace(' ', '-').replace('&', '-').replace(',', '-').replace('/', '-')) #replace special characters with -
            print('Upto {}:'.format(chr(i)), len(businesses))

        for business in businesses:
            for page in range(1, 51):
                yield scrapy.Request(url=url.format(business, page), callback=self.parse, headers=self.headers)


    def parse(self, response):
        page = json.loads(response.body)

        for listing in page['listings']:
            title = listing['name']
            phone = ''
            mobile = ''
            website = ''
            email = ''
            for contact in listing['primaryContacts']:
                if contact['type'] == 'PHONE':
                    phone = contact['value']
                
                elif contact['type'] == 'MOBILE':
                    mobile = contact['value']

                elif contact['type'] == 'URL':
                    website = contact['value']
                
                elif contact['type'] == 'EMAIL':
                    email = contact['value']

            source_url = listing['canonicalUrl']
            description = listing['shortDescriptor']
            if not description:
                description = ''
            category = listing['categoryDescription']
            address = listing['address']
            if address:
                address = address['fullDisplayAddress']
            else:
                address = ''

            data = {
                'Title': title,
                'Category': category,
                'Description': description,
                'Address': address,
                'Phone': phone,
                'Mobile': mobile,
                'Email': email,
                'Website': website,
                'Source URL': source_url
            }

            yield data