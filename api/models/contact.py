"""
The Base class is used to define the common fields that multiple
models will use. It contains the core data attributes that are
shared by all operations involving that entity.

The Create class is derived from the Base class, but allows us to
specify the fields that are needed when creating an instance. It
includes fields necessary for creating a new record, while omitting
fields such as PKs that are auto-generated by the db.

The Response class (no suffix) contains all the data attributes,
including the PK. It is used when returning the response from the
API.

from_attributes = True is essentially the updated version of Pydantic
v1 orm_mode = True. It serves a similar purpose but aims to be more
explicit in its intent.

The orm_mode = True setting allows FastAPI to convert ORM objects
to Pydantic models seamlessly. In short, orm_mode = True is a
convenient way to make Pydantic models compatible with database
models used by ORMs, saving us from manually converting ORM objects
into dictionaries.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class ContactBase(BaseModel):
    account_id: int
    first_name: str
    last_name: str
    title: Optional[str] = None
    email: EmailStr
    primary_phone: Optional[str] = None
    secondary_phone: Optional[str] = None
    site_name: Optional[str] = None
    site_street_1: Optional[str] = None
    site_street_2: Optional[str] = None
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_zipcode: Optional[str] = None
    site_country_id: Optional[int] = None


class ContactCreate(ContactBase):
    """
    The use of pass in the Create classes indicates that the
    Create model does not add any new fields beyond what is
    defined in the Base model. It simply inherits all fields
    from the base model.
    """

    pass


class Contact(ContactBase):
    contact_id: int

    class Config:
        from_attributes = True
