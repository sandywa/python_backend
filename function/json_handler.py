# json/json_handler.py

import json

# Path ke file JSON nasabah
CUSTOMER_JSON_PATH = "./json/customer.json"

# Fungsi untuk membaca data nasabah dari file JSON
def read_customer_data():
    try:
        with open(CUSTOMER_JSON_PATH, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return []

# Fungsi untuk menyimpan data nasabah ke file JSON
def save_customer_data(data):
    with open(CUSTOMER_JSON_PATH, "w") as json_file:
        json.dump(data, json_file, indent=4)
