from pydantic import BaseModel


class CareerRequest(BaseModel):
    job_offer_id: int