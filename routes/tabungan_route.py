# routes/tabungan_route.py

from fastapi import APIRouter, HTTPException, Path, Depends, Header
from datetime import datetime
from typing import List
from models.tabungan import Tabungan, Transaksi, Mutasi
from function.json_handler import read_customer_data, save_customer_data
from function.token_handler import SECRET_KEY, ALGORITHM, verify_token

router = APIRouter()

# Membaca data nasabah dari file JSON saat aplikasi dimulai
registered_customers = read_customer_data()

@router.post("/tabung")
def tabung(data: Tabungan):
    no_rekening = data.no_rekening
    nominal = data.saldo

    # Cari nasabah berdasarkan nomor rekening
    customer = next((c for c in registered_customers if c["no_rekening"] == no_rekening), None)

    if not customer:
        raise HTTPException(status_code=400, detail={"remark": "Nomor rekening tidak dikenali"})

    saldo = customer.get("saldo", 0)

    # Validasi nominal harus lebih dari 0
    if nominal <= 0:
        raise HTTPException(status_code=400, detail={"remark": "Nominal harus lebih dari 0"})

    # Proses penambahan saldo
    customer["saldo"] = saldo + nominal

    # Membuat data transaksi
    transaksi = Transaksi(waktu=datetime.now().isoformat(), kode_transaksi="C", nominal=nominal)
    customer.setdefault("transaksi", []).append(transaksi.dict())

    # Menyimpan data nasabah ke file JSON
    save_customer_data(registered_customers)

    return {"saldo": customer["saldo"]}

@router.post("/tarik")
async def tarik(data: Tabungan, authorization: str = Header(...)):
    no_rekening = data.no_rekening
    nominal = data.saldo

    # Verifikasi token (gunakan token_handler.py yang telah Anda buat)
    try:
        payload = verify_token(authorization)
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail={"remark": "Token tidak valid"})

    # Cari nasabah berdasarkan nomor rekening
    customer = next((c for c in registered_customers if c["no_rekening"] == no_rekening), None)

    if not customer:
        raise HTTPException(status_code=400, detail={"remark": "Nomor rekening tidak dikenali"})

    saldo = customer.get("saldo", 0)

    # Validasi saldo mencukupi
    if saldo < nominal:
        raise HTTPException(status_code=400, detail={"remark": "Saldo tidak mencukupi"})

    # Proses penarikan saldo
    customer["saldo"] = saldo - nominal

    # Membuat data transaksi
    transaksi = Transaksi(waktu=datetime.now().isoformat(), kode_transaksi="D", nominal=nominal)
    customer.setdefault("transaksi", []).append(transaksi.dict())

    # Menyimpan data nasabah ke file JSON
    save_customer_data(registered_customers)

    return {"saldo": customer["saldo"]}

@router.get("/saldo/{no_rekening}")
async def lihat_saldo(no_rekening: str = Path(..., description="Nomor rekening nasabah"), authorization: str = Header(...)):
    # Verifikasi token (gunakan token_handler.py yang telah Anda buat)
    try:
        payload = verify_token(authorization)
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail={"remark": "Token tidak valid"})

    # Cari nasabah berdasarkan nomor rekening
    customer = next((c for c in registered_customers if c["no_rekening"] == no_rekening), None)

    if not customer:
        raise HTTPException(status_code=400, detail={"remark": "Nomor rekening tidak dikenali"})

    saldo = customer.get("saldo", 0)

    return {"saldo": saldo}

@router.get("/mutasi/{no_rekening}")
async def lihat_mutasi(no_rekening: str = Path(..., description="Nomor rekening nasabah"), authorization: str = Header(...)):
    # Verifikasi token (gunakan token_handler.py yang telah Anda buat)
    try:
        payload = verify_token(authorization)
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail={"remark": "Token tidak valid"})

    # Cari nasabah berdasarkan nomor rekening
    customer = next((c for c in registered_customers if c["no_rekening"] == no_rekening), None)

    if not customer:
        raise HTTPException(status_code=400, detail={"remark": "Nomor rekening tidak dikenali"})

    # Membuat daftar mutasi
    mutasi = []

    for transaksi_data in customer.get("transaksi", []):
        transaksi = Transaksi(**transaksi_data)
        mutasi.append(transaksi)

    return Mutasi(mutasi=mutasi)