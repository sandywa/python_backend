# models/customer.py

from pydantic import BaseModel

class CustomerRegistrationRequest(BaseModel):
    nama: str
    nik: str
    no_hp: str

class CustomerRegistrationResponse(BaseModel):
    no_rekening: str
