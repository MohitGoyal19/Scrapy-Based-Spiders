# -*- coding: utf-8 -*-
import scrapy
import requests
import json

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

class HMW(scrapy.Spider):
    name = 'homework_market'
    
    def start_requests(self):
        url = 'https://www.homeworkmarket.com/api/questions?homeworkanswers=true&offset={}&limit=100&popular=true'
        ques_url = 'https://www.homeworkmarket.com/api/object?path='
        for page_no in range(11075):
            page = requests.get(url.format(page_no), headers=headers).json()
            for ques in data['data']:
                link = ques['path']['path']
                yield scrapy.Request(url=ques_url + link.replace('/', '%2F'), headers=headers, callback=self.parse)

    def parse(self, response):
        page = json.loads(response.body)
        question = page['question']['body']
        title = page['question']['title']
        link = index + link
        attachments = ''
        for attachment in page['question']['attachments']:
            attachments = index + attachment['path']['path'] + '\n\n'
        
        yield{
            'Title': title,
            'Question': question,
            'Attachments': attachments,
            'Link': Link
        }