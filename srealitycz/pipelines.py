import collections
import json

import pydantic
import scrapy.exceptions

from . import items


class SrealityczPipeline:
    def process_item(self, item, spider):
        """Validate and save data in JSON Lines file."""
        try:
            item = items.Srealitycz.validate(item)
        except pydantic.ValidationError as err:
            errors = collections.defaultdict(list)
            for error in err.errors():
                field_name = "/".join(str(loc) for loc in error["loc"])
                errors[field_name] = error["msg"]
            raise scrapy.exceptions.DropItem(
                f"Validation has been failed. Item: {item}, errors: {errors}"
            )

        line = json.dumps(item.dict(), ensure_ascii=False, sort_keys=True)
        self.file.write(line + "\n")

    def open_spider(self, spider):
        self.file = open("output.jl", "a")

    def close_spider(self, spider):
        self.file.close()
