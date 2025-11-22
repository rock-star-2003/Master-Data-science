from parsel import Selector
import requests
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
}

links = ['https://amzn.in/d/fIaNEtn']
site = 'Amazon'

class web_scrap:
    def __init__(self):
        self.links = links
        self.site = site

    def start(self):
          for link in links:
                responce = requests.get(link,headers=HEADERS)

                if responce.status_code == 200:
                    product_details =  self.scrap(responce=responce)
                    product_details = json.dumps(product_details, indent=4)
                    print(product_details)
                else:
                      pass
    
    def scrap(self,responce):
          
        data = Selector(responce.text)

        PRODUCT_TITLE = "//span[@id='productTitle']/text()"
        CURRENT_PRICE =   "//span[contains(@class, 'priceToPay')]//span[@class='a-price-whole']/text()"
        LIST_PRICE = "//span[contains(@class, 'basisPrice')]//span[@class = 'a-offscreen']/text()"
        SHIPING_INFO = "//div[@id = 'deliveryBlock_feature_div']/text()"
        OFFER_DETAILS = "//div[contains(@id, 'vsx__offers')]//div[@class = 'offers-items']/text()"
        
        title = self.clean_data(data.xpath(PRODUCT_TITLE).get())
        price = self.clean_prices(data.xpath(CURRENT_PRICE).get())
        listPrice = self.clean_prices(data.xpath(LIST_PRICE).get())
        shipinginfo = self.clean_data(data.xpath(SHIPING_INFO).get())
        couponinfo = self.clean_data(data.xpath(OFFER_DETAILS).get())


        product_details = {
            'ProductTitle' : title ,
            'BrandName' : '',
            'CompetitorSKU' : '',
            'CurrentPrice' : price,
            'ListPrice' : listPrice,
            'ShippingInfo' : shipinginfo,
            'CouponInfo' : couponinfo,
            'StockStatus' : '',
            'EstimatedDelivery' : '',
            'SoldBy' : '',
            'OverallRating' : '',
            'ReviewCount' : '',
            'ScrapeTimestamp' : '',
            'ProductURL' : '',
            'CompetitorWebsite' : '',
        }

        return product_details
    
    def clean_prices(self,raw_price):
        if not raw_price: return 0.0
        
        raw_price = "".join(filter(str.isdigit,raw_price))
        cleaned_string = (
              raw_price.replace('₹','')
              .replace('$','')
              .replace(',','')
         )

        try:
            final_price = float(cleaned_string)
            return final_price
        except ValueError:
            return 0.0
        
    def clean_data(self,raw_data):
        if not raw_data: return ''

        cleaned_data = raw_data.strip()

        return cleaned_data

    
scraping = web_scrap()
scraping.start()





