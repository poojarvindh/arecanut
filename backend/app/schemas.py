from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
    full_name: str


class UserOut(BaseModel):
    username: str
    full_name: str
    role: str


class FarmerLookup(BaseModel):
    farmer_id: str
    farmer_name: str
    mobile_no: str
    gender: str
    age: int
    guardian_name: Optional[str] = None
    village: Optional[str] = None
    taluka: Optional[str] = None
    district: Optional[str] = None


class SurveyIn(BaseModel):
    farmer_id: str
    farmer_name: str
    mobile_no: str
    gender: str
    age: int
    guardian_name: Optional[str] = None

    society_assoc: str
    society_name: Optional[str] = None
    society_since_year: Optional[int] = None
    society_benefits: Optional[str] = None

    village: str
    taluka: str
    district: str

    land_own_acres: float
    land_leased_acres: Optional[float] = 0
    areca_area_acres: float
    areca_plant_count: int

    cultivation_cost_inr: float
    yield_raw_qtl: float

    sale_type: str
    processing_cost_inr: Optional[float] = None
    marketing_channel: str
    rate_inr_per_kg: float
    sale_month: str

    storage_duration_months: Optional[float] = None
    storage_source: Optional[str] = None
    logistics_provider: Optional[str] = None
    logistics_cost_inr_per_qtl: Optional[float] = None

    cultivation_challenges: Optional[str] = None

    crop2_name: Optional[str] = None
    crop2_area_acres: Optional[float] = None
    crop2_yield: Optional[float] = None
    crop2_rate: Optional[float] = None
    crop3_name: Optional[str] = None
    crop3_area_acres: Optional[float] = None
    crop3_yield: Optional[float] = None
    crop3_rate: Optional[float] = None

    mech_owned: Optional[str] = None
    mech_rented: Optional[str] = None
    mech_rental_rate_inr_hr: Optional[str] = None

    credit_linkage: str
    credit_source: Optional[str] = None
    credit_amount_inr: Optional[float] = None
    credit_interest_rate_pct: Optional[float] = None
    credit_repayment_months: Optional[int] = None

    scheme_availed: str
    scheme_name: Optional[str] = None
    scheme_benefits: Optional[str] = None

    irrigation_source: Optional[str] = None
    irrigation_challenges: Optional[str] = None

    soil_test_done: str
    crop_insurance: str
    crop_insurance_detail: Optional[str] = None

    input_source: str
    input_distance_km: Optional[float] = None
    input_challenges: Optional[str] = None

    tech_adoption: str
    tech_adoption_detail: Optional[str] = None

    geo_lat: Optional[float] = None
    geo_long: Optional[float] = None
    field_photo: Optional[str] = None
    enumerator_name: Optional[str] = None
    client_uuid: Optional[str] = None  # set by the app when queued offline, for de-duplication on sync


class SurveyOut(SurveyIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    total_income_inr: float
    entry_timestamp: datetime
    created_by_user_id: Optional[int] = None
