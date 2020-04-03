# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest

class ecb_spider(scrapy.Spider):
    name = 'ecb_spider'
    
    def start_requests(self):
        urls = ['https://portal.ecb.com.au/login']

        for url in urls:
            yield scrapy.Request(url=url, method='GET', callback=self.parse)

    def parse(self, response):
        token = response.css('meta[name="csrf-token"]::attr(content)').get()
        data = {'_token': token, 'email': 's4c0001', 'password': 'VEHICLE1', 'remember': '1'}

        return FormRequest.from_response(response=response, method= 'POST', formdata=data, callback=self.get_urls)

    def get_urls(self, response):
        url = 'https://portal.ecb.com.au/products/'
        
        for i in range(0, 200000):
            yield scrapy.Request(url=url+str(i), callback=self.get_data)

    def get_data(self, response):
        title = response.css('h1::text').get()
        if not title:
            return

        product_id = response.url.split('/')[-1]
        notice = response.css('div.alert.alert-info::text').get()
        product_data = response.css('div.breadcrumb::text').get()
        description = '\n'.join(response.css('div.products--wrapper.p-4::text').extract())
        rrp = response.css('div.col-8 h5::text').extract()[0]
        your_price = response.css('div.col-8 h5::text').extract()[1].css('span::attr(data-price)')

        total_product_weight = response.css('tr td:nth-child(1)::text').extract()[1]
        net_weight_added = response.css('tr td:nth-child(1)::text').extract()[2]
        width = response.css('tr td:nth-child(1)::text').extract()[3]
        dist_front = response.css('tr td:nth-child(1)::text').extract()[4]
        centre_tube_height = response.css('tr td:nth-child(1)::text').extract()[5]
        grill = response.css('tr td:nth-child(1)::text').extract()[6]
        min_centre_tube_width = response.css('tr td:nth-child(1)::text').extract()[7]
        max_centre_tube_width = response.css('tr td:nth-child(1)::text').extract()[8]
        spot_tab = response.css('tr td:nth-child(1)::text').extract()[9]
        fitting_time = response.css('tr td:nth-child(1)::text').extract()[10]
        fitting_instructions = response.css('tr td:nth-child(1)').extract()[11].css('a::attr(href)')
        fitting_video = response.css('tr td:nth-child(1)').extract()[12].css('a::attr(href)')
        retail_spec = response.css('tr td:nth-child(1)').extract()[13].css('a::attr(href)')
        retail_video = response.css('tr td:nth-child(1)').extract()[14].css('a::attr(href)')
        sales_brochure = response.css('tr td:nth-child(1)').extract()[15].css('a::attr(href)')

        data = {'Product_ID': product_id, 
                'title': title, 
                'Product Details': product_data, 
                'Notice': notice, 
                'Desciption': description, 
                'RRP': rrp, 
                'Your Price': your_price, 
                'Total Product Weight': total_product_weight, 
                'Net Weight Added to Vehicle': net_weight_added, 
                'Width of Bar (mm)': width,
                'Distance Added to Front of Vehicle (mm)': dist_front,
                'Centre Tube Height Clearance (mm)': centre_tube_height,
                'Grill Clearance (mm)': grill,
                'Minimum Centre Tube Inside Width (mm)': min_centre_tube_width,
                'Maximum Centre Tube Inside Width (mm)': max_centre_tube_width,
                'Spot Tab Centre to Centre (mm)': spot_tab,
                'Fitting Time': fitting_time,
                'Fitting Instructions': fitting_instructions,
                'Fitting Video': fitting_video,
                'Retail Spec': retail_spec,
                'Retail Video': retail_video,
                'Sales Brochure': sales_brochure
                }
        
        print(data)

        yield data
