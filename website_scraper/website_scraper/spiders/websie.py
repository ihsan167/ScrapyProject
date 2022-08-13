import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
import regex as re

MonthDict = {
'Januari': 'January', 'Februari':'February', 'Mac':'March', 
'April':'April','Mei':'May', 'Jun':'June', 'Julai':'July', 
'Ogos':'August', 'September':'September','Oktober':'October', 
"November":'November','Disember':'December'
}

def keymap_replace(
    string: str, 
    mappings: dict,
    lower_keys=False,
    lower_values=False,
    lower_string=False,
    ) -> str:

    """Replace parts of a string based on a dictionary.

    This function takes a string a dictionary of
    replacement mappings. For example, if I supplied
    the string "Hello world.", and the mappings 
    {"H": "J", ".": "!"}, it would return "Jello world!".

    Keyword arguments:
    string       -- The string to replace characters in.
    mappings     -- A dictionary of replacement mappings.
    lower_keys   -- Whether or not to lower the keys in mappings.
    lower_values -- Whether or not to lower the values in mappings.
    lower_string -- Whether or not to lower the input string.
    """
    replaced_string = string.lower() if lower_string else string

    for character, replacement in mappings.items():

        replaced_string = replaced_string.replace(
            character.lower() if lower_keys else character,
            replacement.lower() if lower_values else replacement
        )

    return replaced_string

class WebsieSpider(CrawlSpider):
    name = 'websie'
    allowed_domains = ['www.utusan.com.my']
    start_urls = ['https://www.utusan.com.my/nasional/2022/07/parlimen-harga-ubat-mungkin-naik-khairy/']




    rules = [
        Rule(LinkExtractor(allow = r'/category/' ), follow = True),
        Rule(LinkExtractor(allow = r'\/\d{4}\/\d{2}\/' ), callback = 'parse_article', follow = True,),
        
            
            
            ]


    def parse_article(self, response):
        
            title = response.xpath('//h1/text()').get(),
            author = response.xpath('//li/span/text()').getall()[0].replace('Oleh','').strip(),
            date =  datetime.strptime(keymap_replace(response.xpath('//li/span/text()').getall()[1], MonthDict),'%d %B %Y, %I:%M %p'),
            category = re.search(r'/([a-zA-Z])+-?([a-zA-Z0-9])*/',response.url).group()[1:-1],    
            url = response.url,

            if (response.xpath('//div/p/span/text()').get() is None) or (response.xpath('//div/p/span/text()').get() =='\xa0'):
                contentWord = re.sub(r'[^\w\s]',""," ".join(response.xpath('//div/p/text()').getall()))
                print('\n\n\n --- AAAAAA --- \n\n\n')
            else : 
                contentWord = re.sub(r'[^\w\s]',""," ".join(response.xpath('//div/p/span/text()').getall()))
                print('\n\n\n +++ BBBBB +++ \n\n\n')
            #'location':re.search(r'^\w+\s?\w*',response.xpath('//div/p/span/text()').get()).group(),
        
            #'contentWord':re.sub(r'[^\w\s]',""," ".join(response.xpath('//div/p/text()').getall())),
            #'location':re.search(r'^\w+\s?\w*',response.xpath('//div/p/text()').get()).group(),
            
            yield {
                'title': title,
                'author': author,
                'date': date,
                'category': category,
                'url' : url,
                'content': contentWord 
            }

            
            
    


    

