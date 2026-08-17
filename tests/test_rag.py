from rag_engine import generate_rag_response

questions = [
    "Can I cancel my order before shipping?",
    "When will I get my refund?",
    "I was charged twice",
    "Do you offer lifetime warranty?"
]

for q in questions:
    print("\n" + "="*60)
    print("Question:", q)

    # answer, docs = generate_rag_response(q)

    # print("\nRetrieved Chunks:")
    # for i, d in enumerate(docs, 1):
    #     print(f"[{i}] {d.page_content}")

    # including citations 

    answer, sources = generate_rag_response(q)

    print(answer)
    
    print("\nSources:")
    for i, s in enumerate(sources, 1):
      print(f"[{i}] {s}")

    print("\nAnswer:")
    print(answer)

# Question: Can I cancel my order before shipping?

# Retrieved Chunks:
# [1] Orders can be cancelled before shipment. If payment has already been captured, cancellation may not be possible.
# [2] SHIPPING POLICY 
# Shipping delays may occur during holidays and weekends.

# Answer:
# Orders can be cancelled before shipment. If payment has already been captured, cancellation may not be possible.

# ============================================================
# Question: When will I get my refund?

# Retrieved Chunks:
# [1] REFUND POLICY 
# Refunds are issued within 5 business days after approval.
# [2] RETURN POLICY 
# Electronics can be returned within 30 days of delivery if unopened.

# Answer:
# Refunds are issued within 5 business days after approval.

# ============================================================
# Question: I was charged twice

# Retrieved Chunks:
# [1] Duplicate charges may occur due to temporary authorization holds and are usually reversed automatically.
# [2] PAYMENT POLICY

# Answer:
# Duplicate charges may occur due to temporary authorization holds and are usually reversed automatically.

# ============================================================
# Question: Do you offer lifetime warranty?

# Retrieved Chunks:
# [1] RETURN POLICY 
# Electronics can be returned within 30 days of delivery if unopened.
# [2] CANCELLATION POLICY

# Answer:
# I could not find this information in the company policies.


# // for the updated retrieval the outptut is::
# Question: Can I cancel my order before shipping?
# Retrieved Chunks:
# [1] Orders can be cancelled before shipment. If payment has already been captured, cancellation may not be possible.

# Answer:
# Orders can be cancelled before shipment.

# ============================================================
# Question: When will I get my refund?
# Retrieved Chunks:
# [1] REFUND POLICY 
# Refunds are issued within 5 business days after approval.

# Answer:
# Refunds are issued within 5 business days after approval.

# ============================================================
# Question: I was charged twice
# Retrieved Chunks:
# [1] Duplicate charges may occur due to temporary authorization holds and are usually reversed automatically.

# Answer:
# Duplicate charges may occur due to temporary authorization holds and are usually reversed automatically.

# ============================================================
# Question: Do you offer lifetime warranty?
# No relevant docs were retrieved using the relevance score threshold 0.4

# Retrieved Chunks:

# Answer:
# I could not find this information in the company policies.
