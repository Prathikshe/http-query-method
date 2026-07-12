from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from data import TRANSACTIONS
from models import TransactionSearchRequest
from search import search_transactions

app = FastAPI(title="QueryAPI - Payment Transaction Search")

# QUERY is a non-"simple" method, so cross-origin browser clients will
# preflight it — CORSMiddleware needs QUERY listed explicitly or the
# preflight OPTIONS response will reject it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["QUERY", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


def handle_search(body: TransactionSearchRequest, response: Response):
    results, total = search_transactions(TRANSACTIONS, body)
    response.headers["Cache-Control"] = "private, max-age=30"  # safe to cache — it's a read
    return {"results": results, "total": total, "page": body.page, "pageSize": body.pageSize}


# Primary route: QUERY /api/transactions
# api_route takes an arbitrary method list, so QUERY doesn't need any special
# framework support the way GET/POST/PUT get via @app.get/@app.post.
@app.api_route("/api/transactions", methods=["QUERY"])
async def query_transactions(body: TransactionSearchRequest, response: Response):
    return handle_search(body, response)


@app.get("/api/transactions")
async def reject_get():
    raise HTTPException(
        status_code=405,
        detail="Use QUERY (or POST /api/transactions/search) for filtered transaction search.",
        headers={"Allow": "QUERY, POST"},
    )


# Fallback for clients/SDKs that can't send a QUERY request yet
@app.post("/api/transactions/search")
async def search_transactions_fallback(body: TransactionSearchRequest, response: Response):
    return handle_search(body, response)
