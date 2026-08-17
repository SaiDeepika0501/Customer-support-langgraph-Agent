from eval_cases import EVAL_CASES
from graph.final_workflow import graph
from dotenv import load_dotenv
load_dotenv()

import os
print("Tracing:", os.getenv("LANGCHAIN_TRACING_V2"))
print("Project:", os.getenv("LANGCHAIN_PROJECT"))

passed = 0

for case in EVAL_CASES:
    result = graph.invoke({
        "query": case["query"],
        "revision_count": 0
    })

    answer = result["answer"].lower()

    ok = all(
        kw.lower() in answer
        for kw in case["expected_keywords"]
    )

    print("\nQ:", case["query"])
    print("A:", result["answer"])
    print("PASS" if ok else "FAIL")

    if ok:
        passed += 1

score = passed / len(EVAL_CASES) * 100
print(f"\nHelpfulness score: {score:.1f}%")