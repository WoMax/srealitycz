from w3lib import url as w3lib_url

from . import constants


class UrlsMixin:
    @staticmethod
    def property_url(entity_id):
        return constants.ENTITY_URL.format(entity_id)

    @staticmethod
    def search_url(deal_code, prop_code):
        params = {
            "category_main_cb": constants.SEARCH_PARAMS[prop_code],
            "category_type_cb": constants.SEARCH_PARAMS[deal_code],
            "per_page": constants.ITEMS_PER_PAGE,
        }
        url = w3lib_url.add_or_replace_parameters(constants.SEARCH_URL, params)
        return url
