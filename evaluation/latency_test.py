import requests
import statistics

latencies = []

for i in range(30):
    r = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"message": "Where is my order ORD-123?"}
    )

    data = r.json()
    latencies.append(data["latency_ms"])

latencies.sort()

p95 = latencies[int(len(latencies) * 0.95) - 1]

print("Average:", round(statistics.mean(latencies), 2), "ms")
print("Min:", round(min(latencies), 2), "ms")
print("P95:", round(p95, 2), "ms")
print("Max:", round(max(latencies), 2), "ms")


# o/p-->>
# Average: 6.93 ms
# Min: 4.47 ms
# P95: 7.77 ms
# Max: 17.95 ms