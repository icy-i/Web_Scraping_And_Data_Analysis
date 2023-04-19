import scrapy
from .config import API
from scraper_api import ScraperAPIClient
client = ScraperAPIClient(API)
class makaan_spider(scrapy.Spider):
    name = 'MAKAAN'
    allowed_domains = ['www.makaan.com']
    # start_urls=[]
    #url='https://www.makaan.com/listings?listingType=buy&pageType=CITY_URLS&cityName=Hyderabad&cityId=12&templateId=MAKAAN_CITY_LISTING_BUY&sellerRating=3plus&page={}'
    url = 'https://www.makaan.com/hyderabad-residential-property/buy-property-in-hyderabad-city?page={}'
    # for i in range(1,2239):
    #      start_urls.append(url.format(i))
         

#https://www.makaan.com/listings?listingType=buy&pageType=CITY_URLS&cityName=Hyderabad&cityId=12&templateId=MAKAAN_CITY_LISTING_BUY&sellerRating=3plus&page=4
    def start_requests(self):
        for i in range(1,2239):
            yield scrapy.Request(client.scrapyGet(url=self.url.format(i)))

    def parse(self, response):
        properties=response.css('li.cardholder')
        for property in properties:
            title= ' '.join(property.css('div.title-line  a[data-type="listing-link"] strong span::text').getall())
            projectname= property.css('div.title-line  strong a.projName span::text').get()
            builder= property.css('a.seller-name span::text').get()
            val=float(property.css('div[data-type="price-link"] span.val::text').get())
            uni=property.css('div[data-type="price-link"] span.unit::text').get()
            if uni==' L':
                    val=val*100000
            if uni==' Cr':
                    val=val*10000000
            price=int(val)
            per_sqft=property.css('td.lbl.rate::text').get()
            area= property.css('td.size span::text').get()
            status=property.css('tr.hcol.w44 td.val::text').get()
            place=property.css('a.loclink span strong::text').get()
            rating=property.css('div.review-rating-wrap')
            rating=rating.css('div.rating')
            rating=rating.css('div::text').get()

            item={
                'title':title,
                'projectname':projectname,
                'builder':builder,
                'price':price,
                'per_sqft':per_sqft,
                'area':area,
                'status':status,
                'place':place,
                'rating':rating,
            }
            yield item
       