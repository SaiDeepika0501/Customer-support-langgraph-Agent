from graph.final_workflow import graph
from eval_cases import EVAL_CASES

grounded = 0

for case in EVAL_CASES:
    result = graph.invoke({
        "query": case["query"],
        "revision_count": 0
    })

    answer = result["answer"].lower()

    # context = (
    #     result.get("rag_context", "") + " " +
    #     result.get("order_status", "")
    # ).lower()

    context = (
    result.get("rag_context", "") + " " +
    result.get("order_status", "") + " " +
    str(result.get("refund_amount", ""))+" "+
    result.get("refund_note","")
    ).lower()

    # Simple heuristic: every sentence in answer should contain
    # at least one word from context
    supported = True

    for sentence in answer.split("."):
        sentence = sentence.strip()

        if not sentence:
            continue

        words = [w for w in sentence.split() if len(w) > 4]

        if words and not any(w in context for w in words):
            supported = False

    print(case["query"], "GROUNDED" if supported else "UNGROUNDED")

    if supported:
        grounded += 1

score = grounded / len(EVAL_CASES) * 100
print(f"Groundedness score: {score:.1f}%")