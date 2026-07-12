# Mock transaction ledger. In a real system this would be a DB query.
TRANSACTIONS = [
    {"id": "txn_001", "date": "2026-01-05", "amount": 250.00, "status": "completed", "paymentMethod": "card", "customerEmail": "john@example.com", "cardLast4": "4242", "merchantId": "M123", "currency": "USD"},
    {"id": "txn_002", "date": "2026-01-18", "amount": 4200.00, "status": "refunded", "paymentMethod": "upi", "customerEmail": "john@example.com", "cardLast4": None, "merchantId": "M123", "currency": "USD"},
    {"id": "txn_003", "date": "2026-02-02", "amount": 89.99, "status": "failed", "paymentMethod": "card", "customerEmail": "priya@example.com", "cardLast4": "1881", "merchantId": "M456", "currency": "EUR"},
    {"id": "txn_004", "date": "2026-02-14", "amount": 1500.00, "status": "completed", "paymentMethod": "card", "customerEmail": "sam@example.com", "cardLast4": "4242", "merchantId": "M123", "currency": "USD"},
    {"id": "txn_005", "date": "2026-03-01", "amount": 320.50, "status": "completed", "paymentMethod": "upi", "customerEmail": "anita@example.com", "cardLast4": None, "merchantId": "M789", "currency": "INR"},
    {"id": "txn_006", "date": "2026-03-22", "amount": 99.00, "status": "pending", "paymentMethod": "card", "customerEmail": "john@example.com", "cardLast4": "4242", "merchantId": "M456", "currency": "USD"},
    {"id": "txn_007", "date": "2026-04-09", "amount": 2750.00, "status": "completed", "paymentMethod": "bank_transfer", "customerEmail": "sam@example.com", "cardLast4": None, "merchantId": "M123", "currency": "USD"},
    {"id": "txn_008", "date": "2026-04-30", "amount": 45.25, "status": "refunded", "paymentMethod": "card", "customerEmail": "priya@example.com", "cardLast4": "1881", "merchantId": "M456", "currency": "EUR"},
    {"id": "txn_009", "date": "2026-05-11", "amount": 610.00, "status": "completed", "paymentMethod": "upi", "customerEmail": "anita@example.com", "cardLast4": None, "merchantId": "M789", "currency": "INR"},
    {"id": "txn_010", "date": "2026-05-19", "amount": 3999.99, "status": "completed", "paymentMethod": "card", "customerEmail": "john@example.com", "cardLast4": "4242", "merchantId": "M123", "currency": "USD"},
    {"id": "txn_011", "date": "2026-06-02", "amount": 150.00, "status": "failed", "paymentMethod": "card", "customerEmail": "sam@example.com", "cardLast4": "9999", "merchantId": "M456", "currency": "USD"},
    {"id": "txn_012", "date": "2026-06-15", "amount": 780.00, "status": "completed", "paymentMethod": "bank_transfer", "customerEmail": "priya@example.com", "cardLast4": None, "merchantId": "M789", "currency": "EUR"},
    {"id": "txn_013", "date": "2026-06-28", "amount": 25.00, "status": "pending", "paymentMethod": "upi", "customerEmail": "anita@example.com", "cardLast4": None, "merchantId": "M123", "currency": "INR"},
    {"id": "txn_014", "date": "2026-07-03", "amount": 5000.00, "status": "completed", "paymentMethod": "card", "customerEmail": "john@example.com", "cardLast4": "4242", "merchantId": "M123", "currency": "USD"},
    {"id": "txn_015", "date": "2026-07-10", "amount": 60.00, "status": "refunded", "paymentMethod": "card", "customerEmail": "sam@example.com", "cardLast4": "4242", "merchantId": "M456", "currency": "USD"},
]
