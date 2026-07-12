# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

QueryAPI: a demo of the HTTP **`QUERY`** method (a body-bearing but safe/idempotent/cacheable verb, unlike `POST`) applied to a payment transaction search/reconciliation endpoint. The same API is implemented twice, in lockstep:

- [`node-express/`](node-express) — Express (Node.js)
- [`fastapi-python/`](fastapi-python) — FastAPI (Python)

Both expose an identical contract: `QUERY /api/transactions` with a `POST /api/transactions/search` fallback, the same request/response JSON shape, and the same 15-row mock dataset. **Any change to filtering behavior, request fields, or response shape must be ported to both implementations** — they are meant to stay interchangeable (see the README's "both examples run unchanged against either implementation" claim).

## Commands

### Node/Express (port 3000)
```bash
cd node-express
npm install
npm start          # node server.js
npm run dev         # node --watch server.js (auto-restart)
```

### FastAPI (port 8000)
```bash
cd fastapi-python
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

There is no test suite or lint config in either implementation. Verify changes by hitting the endpoint with curl (see below) — most HTTP clients/browsers don't have a shortcut for the `QUERY` verb, so use `curl -X QUERY`.

```bash
curl -X QUERY http://localhost:3000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"merchantId": "M123", "currency": "USD", "cardLast4": "4242", "paymentMethod": ["card"], "page": 1, "pageSize": 10}'
```

A plain `GET` on `/api/transactions` should return `405` with an `Allow: QUERY, POST` header in both implementations — this is a deliberate part of the contract, not an oversight.

## Architecture

Both implementations follow the same three-layer split:

| Layer | Node/Express | FastAPI |
|---|---|---|
| Route/handler | `server.js` | `main.py` |
| Request/response shape | inferred from destructured `req.body` | `models.py` (Pydantic: `TransactionSearchRequest`, `DateRange`, `AmountRange`) |
| Filtering logic | `utils/search.js` (`searchTransactions`) | `search.py` (`search_transactions`) |
| Mock data | `data/transactions.js` | `data.py` (`TRANSACTIONS`) |

Filtering is in-memory array filtering (no DB) — `dateRange`/`amountRange` are inclusive bounds, `status`/`paymentMethod` are OR-matched lists, `customerEmail`/`currency` are case-insensitive equality, and pagination is simple slicing after filtering. Both `search.js` and `search.py` implement identical logic; **keep them in sync field-for-field** when adding a filter.

### Why QUERY instead of GET/POST

This isn't incidental — it's the point of the repo (see root [README.md](README.md)). Sensitive filters (email, card last-4) need to stay out of URLs/logs, which rules out `GET`; but the response still needs to be cacheable and safe to auto-retry, which rules out `POST`. `QUERY` gets both. When touching route registration, preserve this:

- **Node** (`server.js`): registers via `app.all()` + a manual `req.method === 'QUERY'` check rather than a hypothetical `app.query()`, so it works regardless of whether the installed Express version has native QUERY support.
- **FastAPI** (`main.py`): registers via `@app.api_route("/api/transactions", methods=["QUERY"])` rather than a `@app.get`/`@app.post` decorator, since there's no `@app.query` shortcut.
- **CORS**: `QUERY` is a non-"simple" method, so cross-origin browsers preflight it. Both CORS configs (the manual OPTIONS middleware in `server.js`, `CORSMiddleware` in `main.py`) explicitly list `QUERY` in allowed methods — if this is dropped, browser (not curl) clients will silently fail preflight.
- **Caching**: both handlers set `Cache-Control: private, max-age=30` on success responses since the request is a safe read, unlike an equivalent `POST`.

### FastAPI-specific note

`/docs` (Swagger UI) is generated from Starlette's `APIRoute` and may not render the custom `QUERY` method correctly — don't rely on it for testing this endpoint; use curl instead.
