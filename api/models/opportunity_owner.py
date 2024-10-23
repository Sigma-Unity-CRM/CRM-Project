from pydantic import BaseModel


class OpportunityOwner(BaseModel):
    opportunity_id: int
    user_id: int

    class Config:
        orm_mode = True
