from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
Return Policy:
Electronics can be returned within 30 days of delivery if unopened.

Refund Policy:
Refunds are issued within 5 business days after approval.

Cancellation Policy:
Orders can be cancelled before shipment. If payment has already been captured, cancellation may not be possible.

Shipping Policy:
Shipping delays may occur during holidays and weekends.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=120,
    chunk_overlap=30
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, 1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)



    
# --- Chunk 1 ---
# Return Policy:
# Electronics can be returned within 30 days of delivery if unopened.

# --- Chunk 2 ---
# Refund Policy:
# Refunds are issued within 5 business days after approval.

# --- Chunk 3 ---
# Cancellation Policy:

# --- Chunk 4 ---
# Orders can be cancelled before shipment. If payment has already been captured, cancellation may not be possible.

# --- Chunk 5 ---
# Shipping Policy:
# Shipping delays may occur during holidays and weekends.