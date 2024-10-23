from pydantic import BaseModel


class ActivityContact(BaseModel):
    activity_id: int
    contact_id: int

    class Config:
        orm_mode = True
