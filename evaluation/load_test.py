import asyncio
import httpx
import time

async def send(i):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "http://127.0.0.1:8000/chat",
            json={"message": f"Where is my order ORD-{i}?"}
        )
        print(i, r.status_code)

async def main():
    start = time.perf_counter()

    await asyncio.gather(*(send(i) for i in range(20)))

    duration = time.perf_counter() - start

    print(f"\nTotal time: {duration:.2f}s")
    print(f"Throughput: {20/duration:.2f} req/s")

asyncio.run(main())

#  python load_test.py
# 0 200
# 7 200
# 13 200
# 8 200
# 1 200
# 6 200
# 11 200
# 9 200
# 10 200
# 12 200
# 4 200
# 5 200
# 3 200
# 17 200
# 2 200
# 16 200
# 15 200
# 19 200
# 18 200
# 14 200

# Total time: 23.23s
# Throughput: 0.86 req/s