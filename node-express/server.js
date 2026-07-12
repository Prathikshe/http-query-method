const express = require('express');
const transactions = require('./data/transactions');
const { searchTransactions } = require('./utils/search');

const app = express();
app.use(express.json());

// QUERY is a non-"simple" method, so cross-origin browser clients will
// preflight it — the OPTIONS response has to allow it explicitly.
app.use((req, res, next) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'QUERY, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.sendStatus(204);
  next();
});

function handleTransactionSearch(req, res) {
  const {
    dateRange,
    amountRange,
    status,
    paymentMethod,
    customerEmail,
    cardLast4,
    merchantId,
    currency,
    page = 1,
    pageSize = 20,
  } = req.body || {};

  const { results, total } = searchTransactions(transactions, {
    dateRange, amountRange, status, paymentMethod,
    customerEmail, cardLast4, merchantId, currency,
    page, pageSize,
  });

  res.set('Cache-Control', 'private, max-age=30'); // safe to cache — it's a read
  res.json({ results, total, page, pageSize });
}

// Primary route: QUERY /api/transactions
// Using app.all + a manual method check instead of app.query() keeps this
// working regardless of whether the running Node/Express version already
// recognizes QUERY as a first-class verb.
app.all('/api/transactions', (req, res, next) => {
  if (req.method === 'QUERY') return handleTransactionSearch(req, res);
  if (req.method === 'GET') {
    return res
      .status(405)
      .set('Allow', 'QUERY, POST')
      .json({ error: 'Use QUERY (or POST /api/transactions/search) for filtered transaction search.' });
  }
  next();
});

// Fallback for clients/SDKs that can't send a QUERY request yet
app.post('/api/transactions/search', handleTransactionSearch);

app.use((req, res) => res.status(404).json({ error: 'Not found' }));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`QueryAPI (Node/Express) listening on http://localhost:${PORT}`);
});
