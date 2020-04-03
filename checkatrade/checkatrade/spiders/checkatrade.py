# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

class CheckatradeSpider(scrapy.Spider):
    name = 'checkatrade'
    links = []
    headers = {'referer': 'https://www.checkatrade.com/', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

    def start_requests(self):
        sitemap = 'https://www.checkatrade.com/SitemapTrades.xml'

        urls = bs(requests.get(sitemap).text, 'html.parser')

        urls = urls.find_all('loc')

        urls = [url.text for url in urls]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    
    def cfDecodeEmail(self, encodedString):
        r = int(encodedString[:2],16)
        email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
        return email

    def primary_skill(self, url):
        response = requests.get(url+'Services.aspx')    
        page = bs(response.text, 'html.parser')
        primary_skill = page.select('.member-services__pri-skills span span')
        if primary_skill:
            primary_skill = primary_skill[0].text
        else:
            primary_skill = ''

        return primary_skill

    def checks(self, url):
        response = requests.get(url+'Checks.aspx')    
        page = bs(response.text, 'html.parser')
        if page.find('span', {'id': 'ctl00_ctl00_content_content_lblInterview'}):
            duration = str(2019 - int(page.find('span', {'id': 'ctl00_ctl00_content_content_lblInterview'}).text)) + ' year(s)'
        else:
            duration = ''

        return duration

    def parse(self, response):
        title = response.css('h1::text').extract_first()
        if title == 'Please try another search.':
            return

        contact_name = response.css('div.contact-card__contact-name::text').extract_first().strip()

        contact = response.css('span[id="ctl00_ctl00_content_lblTelNo"]::text').extract_first()
        if not contact:
            contact = response.css('span[id="ctl00_ctl00_content_lblLandline"]::text').extract_first()
        if not contact:
            contact = response.css('span[id="ctl00_ctl00_content_NormalContactPanel"]::text').extract_first()

        mobile = response.css('span[id="ctl00_ctl00_content_lblMobile"]::text').extract_first()

        email = response.css('a[id="ctl00_ctl00_content_managedEmail"]::attr(href)').extract_first()
        if email:
            email = self.cfDecodeEmail(email.split('#')[1])

        website = response.css('a[id="ctl00_ctl00_content_ctlWeb2"]::attr(href)').extract_first()
    
        address = response.css('div[id="ctl00_ctl00_content_content_pnlBasedIn"] div[class="address"] span::text').extract_first()

        primary_skill = self.primary_skill(response.url)

        duration = self.checks(response.url)

        data = {
            'title': title,
            'contact_name': contact_name,
            'contact': contact,
            'mobile': mobile,
            'email': email,
            'website': website,
            'address': address,
            'primary_skill': primary_skill,
            'duration': duration,
            'source_url': response.url
        }

        self.log(data)

        yield{
            'title': title,
            'contact_name': contact_name,
            'contact': contact,
            'mobile': mobile,
            'email': email,
            'website': website,
            'address': address,
            'primary_skill': primary_skill,
            'duration': duration,
            'source_url': response.url
        }              