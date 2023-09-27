# routes/customer_route.py

from fastapi import APIRouter, HTTPException
from models.customer import CustomerRegistrationRequest, CustomerRegistrationResponse
from function.json_handler import read_customer_data, save_customer_data

router = APIRouter()

# Membaca data nasabah dari file JSON saat aplikasi dimulai
registered_customers = read_customer_data()

@router.post("/daftar", response_model=CustomerRegistrationResponse)
def daftar(nasabah: CustomerRegistrationRequest):
    # Mengecek apakah NIK atau no_hp sudah digunakan
    if any((c["nik"] == nasabah.nik or c["no_hp"] == nasabah.no_hp) for c in registered_customers):
        raise HTTPException(status_code=400, detail={"remark": "NIK atau no_hp sudah digunakan"})

    # Menghasilkan nomor rekening baru (Anda dapat mengganti logika ini sesuai kebutuhan)
    no_rekening = generate_new_account_number()

    # Membuat respons dan menyimpan data nasabah
    response_data = {"no_rekening": no_rekening}
    registered_customers.append({**nasabah.dict(), "no_rekening": no_rekening})

    # Menyimpan data nasabah ke file JSON
    save_customer_data(registered_customers)

    return response_data

# Fungsi untuk menghasilkan nomor rekening baru (contoh sederhana)
def generate_new_account_number():
    return str(len(registered_customers) + 1)