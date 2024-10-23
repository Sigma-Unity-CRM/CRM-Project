from pydantic import BaseModel


class OpportunityContact(BaseModel):
    opportunity_id: int
    contact_id: int

    class Config:
        orm_mode = True
