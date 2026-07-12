# QueryAPI — FastAPI (Payment Transaction Search)

Implements the transaction search/reconciliation endpoint using the HTTP `QUERY`
method: complex filters in a JSON body (not the URL), read-only semantics, and
a cacheable response.

## Run

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Server listens on `http://localhost:8000`.

## Try it

Most HTTP clients don't have a shortcut for QUERY yet — use curl's `-X`:

```bash
curl -X QUERY http://localhost:8000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "dateRange": { "from": "2026-01-01", "to": "2026-06-30" },
    "amountRange": { "min": 100, "max": 5000 },
    "status": ["completed", "refunded"],
    "paymentMethod": ["card", "upi"],
    "customerEmail": "john@example.com"
  }'
```

Fallback for clients that can't send QUERY:

```bash
curl -X POST http://localhost:8000/api/transactions/search \
  -H "Content-Type: application/json" \
  -d '{"merchantId": "M123", "currency": "USD"}'
```

Hitting it with plain `GET` returns `405` with an `Allow: QUERY, POST` header.

## Endpoint

`QUERY /api/transactions` (fallback: `POST /api/transactions/search`)

Body fields (all optional, see `models.py`):

| field | type |
|---|---|
| `dateRange` | `{ from, to }` (ISO date strings) |
| `amountRange` | `{ min, max }` |
| `status` | `string[]` |
| `paymentMethod` | `string[]` |
| `customerEmail` | `string` |
| `cardLast4` | `string` |
| `merchantId` | `string` |
| `currency` | `string` |
| `page` | `int` (default `1`) |
| `pageSize` | `int` (default `20`) |

Response: `{ results, total, page, pageSize }`.

Note: FastAPI's interactive docs (`/docs`) are generated from Starlette's
`APIRoute` and may not render a custom `QUERY` method correctly in Swagger UI —
test with curl or a HTTP client that supports arbitrary methods instead.
