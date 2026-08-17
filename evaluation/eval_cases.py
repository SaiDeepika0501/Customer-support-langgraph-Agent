EVAL_CASES = [
    {
        "query": "What is your refund policy?",
        "expected_keywords": ["5 business days", "approval"],
        "must_refuse": False
    },
    {
        "query": "Can I return an unopened item?",
        "expected_keywords": ["30 days", "unopened"],
        "must_refuse": False
    },
    {
        "query": "Do you offer lifetime warranty?",
        "expected_keywords": [],
        "must_refuse": True
    },
    {
        "query": "Where is my order ORD-123?",
        "expected_keywords": ["ORD-123", "Out for delivery"],
        "must_refuse": False
    },
    {
        "query": "I was charged twice",
        "expected_keywords": ["refund", "authorization hold"],
        "must_refuse": False
    }
]