from fastapi import FastAPI
from app.routers.userRoute import router as router_user
from app.routers.accountRoute import router as route_account
from app.routers.currencyRoute import router as route_currency
from app.routers.categoryRoute import router as route_category
from app.routers.transactionRoute import router as route_transaction
from app.routers.budgetRoute import router as route_budget
from app.core.lifecycle import startup, shutdown
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(on_startup=[startup], on_shutdown=[shutdown])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_user)
app.include_router(route_account)
app.include_router(route_currency)
app.include_router(route_category)
app.include_router(route_transaction)
app.include_router(route_budget)


@app.get("/")
def health_checker():
    return {"message": "API is running ✅"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
