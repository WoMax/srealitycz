ITEMS_PER_PAGE = 999  # max possible value

DEAL_CODES = ["sale", "rent"]
PROPERTY_CODES = ["apartment", "house"]

ENTITY_URL = "https://www.sreality.cz/api/cs/v2/estates/{}"
SEARCH_URL = "https://www.sreality.cz/api/cs/v2/estates"

SEARCH_PARAMS = {
    "apartment": 1,
    "house": 2,
    "sale": 1,
    "rent": 2,
}
