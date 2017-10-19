# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import pandas as pd
import numpy as np

#creating a Scrapy spider to search and return the results of the "free stuff" page for the variable "city"
class FreeTestSpider(scrapy.Spider): 
    name = 'free_test'
    city = 'denver' #making the city a variable so that it is easy to configure
    allowed_domains = ['craigslist.org']
    start_urls = ['https://' + city + '.craigslist.org/d/free-stuff/search/zip/']

    def parse(self, response):
        #load titles and associated dates into variables
        titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        date_time = response.xpath('//time/@datetime').extract()
        
        #debug section
        #print(type(titles))
        #print(type(date_time))

		#build pandas data frame
        matrix = np.column_stack((titles, date_time))
        df = pd.DataFrame(data=matrix, columns=['titles', 'timestamp'])

        #check if file exists
        import os.path
        counter = 0
        for_counter = 0
        file_name = str('test' + str(counter) + '.csv')
        while for_counter == 0 :
	        if os.path.isfile(file_name) :
	        	file_name = str('test' + str(counter) + '.csv')
	        	counter += 1
	        else :
	        	#export
	        	df.to_csv(file_name, header=True, index=False, encoding="utf-8")
	        	for_counter += 1

        #iterate over multiple pages to acquire as many restuls as possible
        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = "https://denver.craigslist.org" + relative_next_url
        yield Request(absolute_next_url, callback=self.parse)
