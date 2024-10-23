from pydantic import BaseModel


class ActivityUser(BaseModel):
    activity_id: int
    user_id: int

    class Config:
        from_attributes = True
