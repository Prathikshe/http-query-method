function searchTransactions(transactions, filters) {
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
  } = filters;

  const filtered = transactions.filter((txn) => {
    if (dateRange?.from && txn.date < dateRange.from) return false;
    if (dateRange?.to && txn.date > dateRange.to) return false;
    if (amountRange?.min != null && txn.amount < amountRange.min) return false;
    if (amountRange?.max != null && txn.amount > amountRange.max) return false;
    if (status?.length && !status.includes(txn.status)) return false;
    if (paymentMethod?.length && !paymentMethod.includes(txn.paymentMethod)) return false;
    if (customerEmail && txn.customerEmail.toLowerCase() !== customerEmail.toLowerCase()) return false;
    if (cardLast4 && txn.cardLast4 !== cardLast4) return false;
    if (merchantId && txn.merchantId !== merchantId) return false;
    if (currency && txn.currency.toLowerCase() !== currency.toLowerCase()) return false;
    return true;
  });

  const total = filtered.length;
  const start = (page - 1) * pageSize;
  const results = filtered.slice(start, start + pageSize);

  return { results, total };
}

module.exports = { searchTransactions };
