from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import date

# Base HR Analytics Query
class HRAnalyticsQuery(BaseModel):
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = []

# HR Analytics Response
class HRAnalyticsResponse(BaseModel):
    answer: str
    query: Optional[str] = None
    result: Optional[str] = None
    analysis: Optional[str] = None

# HR Data Schema
class HRDataBase(BaseModel):
    month: Optional[str] = None
    date: Optional[date] = None
    month_year: Optional[str] = None
    year: Optional[int] = None
    count: Optional[int] = None
    emp_id: Optional[str] = None
    employee_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    date_of_joining: Optional[date] = None
    band: Optional[str] = None
    designation: Optional[str] = None
    process: Optional[str] = None
    voice_non_voice: Optional[str] = None
    account_name: Optional[str] = None
    domain: Optional[str] = None
    department: Optional[str] = None
    manager: Optional[str] = None
    functional_head: Optional[str] = None
    location: Optional[str] = None
    sub_location: Optional[str] = None
    country: Optional[str] = None
    date_of_resignation: Optional[date] = None
    last_working_day: Optional[date] = None
    date_of_intimation_of_attrition: Optional[date] = None
    reason: Optional[str] = None
    voluntary_involuntary: Optional[str] = None
    nascom_attrition_analysis: Optional[str] = None
    new_country: Optional[str] = None
    active_count: Optional[int] = None
    new_hire: Optional[int] = None
    opening_hc: Optional[int] = None
    overall_inactive_count: Optional[int] = None
    inactive_count: Optional[int] = None
    age_group: Optional[str] = None
    tenure_bucket: Optional[str] = None

class HRData(HRDataBase):
    id: int

    class Config:
        orm_mode = True
