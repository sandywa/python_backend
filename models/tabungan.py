# models/tabungan.py

from pydantic import BaseModel
from typing import List

class Transaksi(BaseModel):
    waktu: str
    kode_transaksi: str
    nominal: int

class Tabungan(BaseModel):
    no_rekening: str
    saldo: int
    transaksi: List[Transaksi] = []

class Mutasi(BaseModel):
    mutasi: List[Transaksi]
