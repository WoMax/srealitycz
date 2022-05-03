import math

import scrapy
from w3lib import url as w3lib_url

from .. import constants
from .. import items
from .. import mixins


class SrealityczSpider(scrapy.Spider, mixins.UrlsMixin):
    name = "srealitycz"

    def start_requests(self):
        for deal_code in constants.DEAL_CODES:
            for prop_code in constants.PROPERTY_CODES:
                yield scrapy.Request(
                    url=self.search_url(deal_code, prop_code),
                    cb_kwargs={"deal_code": deal_code, "prop_code": prop_code},
                )

    def parse(self, response, deal_code, prop_code):
        data = response.json()
        total_pages = math.ceil(data["result_size"] / constants.ITEMS_PER_PAGE)

        if total_pages > 1:  # pagination
            yield from self.parse_next_pages(response, total_pages)

        for entity in data["_embedded"]["estates"]:
            entity_id = entity["hash_id"]
            entity_url = self.property_url(entity_id)

            item = items.Srealitycz.construct(
                ID=entity_id,
                URL=entity_url,
                DEAL_CODE=deal_code,
                PROPERTY_CODE=prop_code,
                TITLE=entity["name"],
                ADDRESS=entity["locality"],
            )

            yield scrapy.Request(
                url=entity_url,
                callback=self.parse_entity,
                meta={"item": item},
            )

    def parse_next_pages(self, response, total_pages):
        url = response.url
        for page in range(2, total_pages + 1):
            url = w3lib_url.add_or_replace_parameter(url, "page", page)
            yield scrapy.Request(url=url, cb_kwargs=response.cb_kwargs)

    def parse_entity(self, response):
        data = response.json()
        item = response.meta["item"]
        item.TITLE = data["name"]["value"]
        item.DESCRIPTION = data["text"]["value"]
        item.ADDRESS = data["locality"]["value"]
        item.LONGITUDE_LATITUDE = [data["map"]["lon"], data["map"]["lat"]]

        price = data["price_czk"].get("value")
        if price:
            item.PRICE = f"{price} Kč"

        images = data["_embedded"]["images"]
        if images:
            item.IMAGES = [img["_links"]["self"]["href"] for img in images]

        features = {}
        for feature in data["items"]:
            features[feature["name"]] = self.get_feature_value(feature)

        item.FEATURES = features
        yield item.dict()

    def get_string_value(self, item):
        """
        :param item: dict that contains nested list of values
        :return: string feature value like `7 844 000 Kč za nemovitost`
        """

        value = item["value"]
        if isinstance(value, str):
            for field in ["currency", "unit"]:
                value += " {}".format(item.get(field, ""))
                value = value.strip()

        return value

    def get_feature_value(self, item):
        """
        :param item: dict that contains values data
        :return: list of values data like [`7 844 000 Kč za nemovitost`]
        """
        if item.get("type") == "set":
            return [self.get_string_value(val) for val in item["value"]]

        return [self.get_string_value(item)]
