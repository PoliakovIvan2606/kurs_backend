from typing import Optional

from pydantic import BaseModel, constr, conint


class CarModel(BaseModel):
    number: constr(min_length=7, max_length=11)
    full_name: str
    address: str
    make: str
    date_of_issue: conint(le=2024)
    engine_capacity: conint(gt=0)
    engine_number: constr(min_length=17, max_length=17)
    color: str
    vehicle_type: str
    technical_inspection: bool = True

    organization: Optional['OrganizationModel'] = None

class AddCarModel(BaseModel):
    number: str
    full_name: str
    address: str
    make: str
    date_of_issue: int
    engine_capacity: int
    engine_number: str
    color: str
    vehicle_type: str

    organization_id: Optional[int] = None
class OrganizationModel(BaseModel):
    name: str
    city: str
    area: str
    address: str
    supervisor: str

class AcidentModel(BaseModel):
    data: str
    type_of_incident: str
    place: str
    brands_of_affected_cars: str
    number: str
    machine_type: str
    summary: str
    number_of_victims: int
    amount_of_damage: int
    cause: str
    road_conditions: str
