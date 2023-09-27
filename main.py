# main.py

from fastapi import FastAPI
from routes.customer_route import router as customer_router
from routes.tabungan_route import router as tabungan_router

app = FastAPI()

# Mengimpor dan menggabungkan rute dari customer_route dan tabungan_route
app.include_router(customer_router, prefix="/api/v1/customer")
app.include_router(tabungan_router, prefix="/api/v1/tabungan")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
