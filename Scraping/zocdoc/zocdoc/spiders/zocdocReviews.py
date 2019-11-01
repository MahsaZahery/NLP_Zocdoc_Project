import time
from scrapy import Spider, Request
from zocdoc.items import ZocdocItem
from scrapy_splash import SplashRequest
from scrapy.http import HtmlResponse
from selenium import webdriver


class ZocdocreviewsSpider(Spider):
	name = 'zocdocReviews'
	allowed_url = ['https://www.zocdoc.com']
	start_urls = ['https://www.zocdoc.com/profiles/new-york']

	def parse(self, response):

		links = response.xpath('//a[@class="sc-2gkh1u-3 jBFlDB"]/@href').extract()
		links = ['https://www.zocdoc.com' + link for link in links] 

		for url in links: 
			yield SplashRequest(url=url, callback=self.parse_details, args = {"wait": 2}, endpoint = "render.html") 

	def parse_details(self,response): 

		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--incognito')
		options.add_argument('--headless')
		driver = webdriver.Chrome("/Users/mahsa/Downloads/chromedriver", options=options)

	
		driver.get(str(response).split(" ")[1].split(">")[0])

		more_result_button = driver.find_elements_by_class_name("sc-9l12hz-3")

		for x in range(len(more_result_button)):
			if more_result_button[x].is_displayed():
				driver.execute_script("arguments[0].click();", more_result_button[x])
				time.sleep(1)

		response = HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8')


		doctor = response.xpath('//span[@itemprop="name"]/text()').extract_first()
		doctor_type = response.xpath('//a[@class="sc-1s83c7v-14 etQBIp esebpo-0 QHonW"]/text()').extract_first()


		print(doctor)
		print(doctor_type)
		print("$"*50)

		num_reviews = response.xpath('//button[@class="sc-15uikgc-4 fQcwri yglqz4-2 DGjwB"]/span/text()').extract_first()

		reviews = response.xpath('//div[@class="sc-9l12hz-1 gZBRFb"]')

		for review in reviews:
			text = review.xpath('.//*[@class="sc-1ct2r0d-0 iWexcg"]/span/div/p/span/text()').extract_first()
			name = review.xpath('.//*[@class="sc-1ct2r0d-0 iWexcg"]/span/div/span/span/text()').extract_first()
			rating = review.xpath('.//*[@class="sc-17gvxzw-0 eWWPgI sc-14oxdvn-0 dtrCpT"]/@data-rating').extract()

			item = ZocdocItem()
			
			item['doctor'] = doctor
			item['doctor_type'] = doctor_type
			item['name'] = name
			item['text'] = text
			item['num_reviews'] = num_reviews
			item['rating'] = rating

			yield item
