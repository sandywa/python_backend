# models/account.py

from pydantic import BaseModel

class AccountCustomer(BaseModel):
    username: str
    password: str
    
