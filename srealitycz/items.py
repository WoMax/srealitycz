import html
import typing

import pydantic


class Srealitycz(pydantic.BaseModel):
    ID: str
    PRICE: typing.Optional[str]
    URL: str
    DEAL_CODE: str
    PROPERTY_CODE: str
    TITLE: str
    DESCRIPTION: str
    IMAGES: typing.Optional[typing.List[str]]
    ADDRESS: str
    LONGITUDE_LATITUDE: typing.List[float]
    FEATURES: typing.Dict[str, typing.List[typing.Union[str, bool]]]

    @staticmethod
    def unescape_str(value):
        """Unescape string like `\u00dast\u0159edn\u00ed` into `Ústřední`."""
        if isinstance(value, str):
            return html.unescape(value.replace("\xa0", " "))
        return value

    @pydantic.validator("PRICE", "TITLE", "DESCRIPTION", "ADDRESS", pre=True)
    def unescape_string_value(cls, value):
        return cls.unescape_str(value)

    @pydantic.validator("FEATURES", pre=True)
    def unescape_features_value(cls, feature_dict):
        for key, values in feature_dict.items():
            for idx, value in enumerate(values):
                values[idx] = cls.unescape_str(value)

        return feature_dict
