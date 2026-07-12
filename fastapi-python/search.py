from typing import Any, Dict, List, Tuple

from models import TransactionSearchRequest


def search_transactions(
    transactions: List[Dict[str, Any]], filters: TransactionSearchRequest
) -> Tuple[List[Dict[str, Any]], int]:
    def matches(txn: Dict[str, Any]) -> bool:
        if filters.dateRange:
            if filters.dateRange.from_ and txn["date"] < filters.dateRange.from_:
                return False
            if filters.dateRange.to and txn["date"] > filters.dateRange.to:
                return False
        if filters.amountRange:
            if filters.amountRange.min is not None and txn["amount"] < filters.amountRange.min:
                return False
            if filters.amountRange.max is not None and txn["amount"] > filters.amountRange.max:
                return False
        if filters.status and txn["status"] not in filters.status:
            return False
        if filters.paymentMethod and txn["paymentMethod"] not in filters.paymentMethod:
            return False
        if filters.customerEmail and txn["customerEmail"].lower() != filters.customerEmail.lower():
            return False
        if filters.cardLast4 and txn["cardLast4"] != filters.cardLast4:
            return False
        if filters.merchantId and txn["merchantId"] != filters.merchantId:
            return False
        if filters.currency and txn["currency"].lower() != filters.currency.lower():
            return False
        return True

    filtered = [t for t in transactions if matches(t)]
    total = len(filtered)
    start = (filters.page - 1) * filters.pageSize
    results = filtered[start : start + filters.pageSize]
    return results, total
