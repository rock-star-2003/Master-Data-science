from mongoengine import DynamicDocument, StringField, FloatField
from amazon_settings import (
    PARSE_COLLECTION, CRAWLER_COLLECTION, MONGO_COLLECTION_URL_FAILED
)


class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}

    pdp_url = StringField(required=True, unique=True)
    selling_price = FloatField()
    price_was = FloatField()
    breadcrumb = StringField()
    review = StringField()
    rating = StringField()
    image = StringField()


class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required = True)
    source = StringField(required = True)



