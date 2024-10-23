from pydantic import BaseModel


class Country(BaseModel):
    """
    Represents a Country, with its name, code, and ID.
    """

    country_id: int
    country_name: str
    country_code: str
