<!-- # Evaluation Report

## Environment
- FastAPI + LangGraph + FAISS
- Local development environment

## Dataset
- 25 evaluation queries
- 6 support categories

## Latency
- Average: 6.93 ms
- Min: 4.47 ms
- P95: 7.77 ms
- Max: 17.95 ms

## Retrieval
- Top-3 retrieval accuracy: 100.0%

## Groundedness
- Manual evaluation on 10 representative queries
- Supported answers: 8/10
- Groundedness: 80%

## Reflection
- Manual evaluation on 10 revision-triggering queries
- Improved revised answers: 7/10
- Reflection improvement: 70%

## Concurrency
- 20 concurrent requests tested
- Throughput: 0.86 req/s

## Observed Failure Cases
- Questions outside the policy knowledge base (e.g., lifetime warranty)
- Ambiguous refund queries may require clarification

 -->

 # Evaluation Report

## Environment
- FastAPI + LangGraph + FAISS
- Local development environment

## Dataset
- 25 retrieval evaluation queries
- 5 end-to-end quality evaluation queries

## Retrieval
- Top-3 retrieval accuracy: 100%

## End-to-End Quality
- Helpfulness: 80% (initial)
- Refusal accuracy: 80% (initial)
- Groundedness: 60% (initial)

## Observed Failure Cases
- Unknown policy questions produced clarification instead of refusal.
- Duplicate payment answers lacked explanation of authorization holds.
- Groundedness evaluator did not initially account for tool outputs.

## Improvements Applied
- Added explicit refusal message for unsupported policies.
- Added duplicate-payment explanation and refund guidance.
- Included tool outputs in groundedness evaluation.

## Concurrency
- 20 concurrent requests tested locally
- Throughput: 0.86 req/s

## Latency
- Average: 6.93 ms
- P95: 7.77 ms
- Max: 17.95 ms