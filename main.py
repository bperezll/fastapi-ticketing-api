from fastapi import FastAPI
from routers import orders
from routers import customers, products

app = FastAPI()

app.include_router(router=customers.router)
app.include_router(router=orders.router, prefix="/customers/{customer_id}/orders")
app.include_router(router=products.router)

# fastapi dev main.py