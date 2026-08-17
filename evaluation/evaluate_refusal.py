from eval_cases import EVAL_CASES
from graph.final_workflow import graph

correct = 0

REFUSAL_PATTERNS = [
    "could not find",
    "do not have",
    "not available",
    "cannot confirm"
]

for case in EVAL_CASES:
    result = graph.invoke({
        "query": case["query"],
        "revision_count": 0
    })

    answer = result["answer"].lower()

    refused = any(p in answer for p in REFUSAL_PATTERNS)

    expected = case["must_refuse"]

    ok = (refused == expected)

    print(case["query"], "PASS" if ok else "FAIL")

    if ok:
        correct += 1

score = correct / len(EVAL_CASES) * 100
print(f"Refusal accuracy: {score:.1f}%")