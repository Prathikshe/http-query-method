# QueryAPI

A payment transaction search/reconciliation API built on the HTTP **`QUERY`**
method — complex, sensitive filters travel in a JSON request body instead of
a URL, while the request still keeps GET's safe, read-only, cacheable
semantics. Two equivalent implementations are included:

- [`node-express/`](node-express) — Express (Node.js)
- [`fastapi-python/`](fastapi-python) — FastAPI (Python)

## The `QUERY` method: when and why

`QUERY` closes a gap that's existed in HTTP since the beginning: `GET` is
safe, idempotent, and cacheable but can't carry a body, so params get stuffed
into the URL; `POST` carries a body but isn't safe, idempotent, or cacheable,
so it's the wrong verb for something that's actually just a read. The
[draft](https://datatracker.ietf.org/doc/draft-ietf-httpbis-safe-method-w-body/)
(`draft-ietf-httpbis-safe-method-w-body`) started circulating in the IETF
HTTPBIS working group around 2021, authored by Julian Reschke, James M.
Snell (Cloudflare), and Mike Bishop (Akamai). After 14 revisions it was
approved as **[RFC 10008](https://datatracker.ietf.org/doc/rfc10008/)** in
June 2026 — so `QUERY` is now an official HTTP standard, not just a proposal.

## Description

Transaction search needs a lot of filters at once: date range, amount range,
status, payment method, customer email, card last-4, merchant ID, currency.
`GET` can only express that as a query string, and `POST` is the usual
workaround — but neither is actually correct for a read-only search. `QUERY`
is a request method purpose-built for this: a request body like `POST`, but
safe and idempotent like `GET`.

## Benefits

- **Keeps sensitive filters out of URLs** — no `customerEmail` or `cardLast4`
  leaking into proxy/CDN/load-balancer access logs or browser history, which
  is exactly what PCI/compliance audits flag.
- **No URL length limit** — multi-value filters (several statuses, several
  payment methods, nested ranges) don't fight the ~2KB practical URL cap.
- **Cacheable** — unlike `POST`, `QUERY` is safe/read-only, so responses can
  carry `Cache-Control` and be served from a shared cache.
- **Safe to auto-retry** — proxies, gateways, and WAFs that understand
  `QUERY`'s safe/idempotent semantics can retry a dropped connection without
  risking a duplicate side effect, something never safe to assume for `POST`.

## Difference: GET vs POST vs QUERY

| | `GET` | `POST /search` | `QUERY` |
|---|---|---|---|
| Sensitive filters kept out of URLs/logs | ❌ | ✅ | ✅ |
| No URL length limit for complex filters | ❌ | ✅ | ✅ |
| Cacheable (repeat searches served from cache) | ✅ | ❌ | ✅ |
| Safe to auto-retry on network failure | ✅ | ❌ (risky) | ✅ |
| Signals "read-only, no state change" to proxies/CDNs/WAFs | ✅ | ❌ | ✅ |

`QUERY` is the only option with a full column of checkmarks: it combines
`POST`'s ability to carry a rich body with `GET`'s safe/cacheable/retryable
semantics.

**Where `QUERY` doesn't apply:** initiating a payment, refund, or capture —
those are genuine state changes and stay on `POST`. `QUERY` is for the *read*
side only: search, reconciliation reports, statement lookups, audit trails.

## What's in this repo

Two servers implementing the identical API contract, so you can compare how
`QUERY` support looks in each stack:

- [`node-express/`](node-express) — Express, listens on `:3000`
- [`fastapi-python/`](fastapi-python) — FastAPI, listens on `:8000`

Both expose `QUERY /api/transactions` (plus the `POST
/api/transactions/search` fallback below), filter the same 15-row mock
transaction ledger in memory, and return the same `{ results, total, page,
pageSize }` shape — the curl examples below run unchanged against either
one. See [`node-express/README.md`](node-express/README.md) and
[`fastapi-python/README.md`](fastapi-python/README.md) for per-implementation
setup instructions.

## Examples

Both servers expose the same endpoint: `QUERY /api/transactions` (with a
`POST /api/transactions/search` fallback for clients that can't send `QUERY`
yet).

### Example 1 — multi-filter search

Find completed or refunded card/UPI payments for one customer, in a date and
amount range:

```bash
curl -X QUERY http://localhost:3000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "dateRange": { "from": "2026-01-01", "to": "2026-06-30" },
    "amountRange": { "min": 100, "max": 5000 },
    "status": ["completed", "refunded"],
    "paymentMethod": ["card", "upi"],
    "customerEmail": "john@example.com"
  }'
```

```json
{
  "results": [
    { "id": "txn_001", "date": "2026-01-05", "amount": 250,    "status": "completed", "paymentMethod": "card", "customerEmail": "john@example.com", "cardLast4": "4242", "merchantId": "M123", "currency": "USD" },
    { "id": "txn_002", "date": "2026-01-18", "amount": 4200,   "status": "refunded",  "paymentMethod": "upi",  "customerEmail": "john@example.com", "cardLast4": null,   "merchantId": "M123", "currency": "USD" },
    { "id": "txn_010", "date": "2026-05-19", "amount": 3999.99,"status": "completed", "paymentMethod": "card", "customerEmail": "john@example.com", "cardLast4": "4242", "merchantId": "M123", "currency": "USD" }
  ],
  "total": 3,
  "page": 1,
  "pageSize": 20
}
```

### Example 2 — merchant reconciliation by card + currency

Reconcile one merchant's USD card transactions ending in a specific card,
paginated:

```bash
curl -X QUERY http://localhost:8000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "merchantId": "M123",
    "currency": "USD",
    "cardLast4": "4242",
    "paymentMethod": ["card"],
    "page": 1,
    "pageSize": 10
  }'
```

```json
{
  "results": [
    { "id": "txn_001", "date": "2026-01-05", "amount": 250,     "status": "completed", "paymentMethod": "card", "customerEmail": "john@example.com", "cardLast4": "4242", "merchantId": "M123", "currency": "USD" },
    { "id": "txn_004", "date": "2026-02-14", "amount": 1500,    "status": "completed", "paymentMethod": "card", "customerEmail": "sam@example.com",  "cardLast4": "4242", "merchantId": "M123", "currency": "USD" },
    { "id": "txn_010", "date": "2026-05-19", "amount": 3999.99, "status": "completed", "paymentMethod": "card", "customerEmail": "john@example.com", "cardLast4": "4242", "merchantId": "M123", "currency": "USD" },
    { "id": "txn_014", "date": "2026-07-03", "amount": 5000,    "status": "completed", "paymentMethod": "card", "customerEmail": "john@example.com", "cardLast4": "4242", "merchantId": "M123", "currency": "USD" }
  ],
  "total": 4,
  "page": 1,
  "pageSize": 10
}
```

### Example 3 — POST fallback with a single filter

Every filter field is optional, and clients/SDKs/proxies that can't send a
`QUERY` request yet can hit the `POST` fallback route instead — same filters,
same response shape, just not cacheable or automatically retry-safe the way
`QUERY` is:

```bash
curl -X POST http://localhost:3000/api/transactions/search \
  -H "Content-Type: application/json" \
  -d '{"status": ["pending"]}'
```

```json
{
  "results": [
    { "id": "txn_006", "date": "2026-03-22", "amount": 99,    "status": "pending", "paymentMethod": "card", "customerEmail": "john@example.com",  "cardLast4": "4242", "merchantId": "M456", "currency": "USD" },
    { "id": "txn_013", "date": "2026-06-28", "amount": 25,    "status": "pending", "paymentMethod": "upi",  "customerEmail": "anita@example.com", "cardLast4": null,   "merchantId": "M123", "currency": "INR" }
  ],
  "total": 2,
  "page": 1,
  "pageSize": 20
}
```

All three examples run unchanged against either implementation (Node on
`:3000`, FastAPI on `:8000`) — the request/response shape is identical.
