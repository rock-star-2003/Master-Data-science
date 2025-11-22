import requests
from parsel import Selector
import logging
from mongoengine import connect
from pymongo import MongoClient
from amazon_items import ProductItem, FailedItem
from amazon_settings import (
    HEADERS, MONGO_URI, DB_NAME, CRAWLER_COLLECTION, PARSE_COLLECTION
)


class Parser:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        db = self.client[DB_NAME]
        self.crawler_collection = db[CRAWLER_COLLECTION]
        self.parser_collection = db[PARSE_COLLECTION]
        
    def start(self):
        links = self.crawler_collection.find()

        for link in links:
            link = link.get("url","")
        
            response = requests.get(link, headers=HEADERS)
            
            if response.status_code == 200:
                self.parse_item(response)
            else:
                logging.warning(f"Status code : {response.status_code}")
                FailedItem(url=link, source="parser").save()
    
    def parse_item(self, response):
        sel = Selector(response.text)
        
        PRODUCT_NAME_XPATH = '//h1[@id="title"]/span/text()'
        SELLING_PRICE_XPATH = '//span[@class="a-price-whole"]/text()'
        PRICE_WAS_XPATH = '//span[@class="aok-relative"]//span[@class="a-offscreen"]/text()'
        BREADCRUMB_XPATH = '//div[@id="wayfinding-breadcrumbs_feature_div"]//a/text()'
        REVIEW_XPATH = '//span[@id="acrCustomerReviewText"]/text()'
        RATING_XPATH = '//span[@id="acrPopover"]//a/span/text()'
        IMAGE_XPATH = '//img[@id="landingImage"]/@src'
        
        
        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
        price_was = sel.xpath(PRICE_WAS_XPATH).get()
        breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
        review = sel.xpath(REVIEW_XPATH).get()
        rating = sel.xpath(RATING_XPATH).get()
        image = sel.xpath(IMAGE_XPATH).get()
        
        
        
        product_name = product_name.strip() if product_name else ""
        selling_price = (
            "".join(
                ch for ch in selling_price if ch in "0123456789."
            )
        ) if selling_price else ""
        
        price_was = (
            "".join(
                ch for ch in price_was if ch in "0123456789."
            )
        ) if price_was else ""
        breadcrumb = " > ".join(breadcrumb) if breadcrumb else ""
        review = review.replace("ratings","").strip() if review else ""
        rating = rating.strip() if rating else ""
        image = image if image else ""
        
        
        item = {}
        
        item["product_name"] = product_name
        item["selling_price"] = selling_price
        item["price_was"] = price_was
        item["breadcrumb"] = breadcrumb
        item["review"] = review
        item["rating"] = rating 
        item["image"] = image
        
        logging.info(item)
        
        try:
            ProductItem(**item).save()
        except:
            pass



if __name__ == "__main__":
    parser = Parser()
    parser.start()
