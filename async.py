'''

import asyncio

async def hello():
    print("HELLO")
    a = add(2,3)
    await asyncio.sleep(2)
    world("Hello")
    print(f"The result: {a}")


def add(a,b):
    return (a+b)


def world(string):
    print(f"The string: {string}")


async def goodbye():
    print("GoodBye")
    await asyncio.sleep(1)
    print("See you later")



async def main():
    await asyncio.gather(hello(), goodbye())

asyncio.run(main())


'''


import asyncio
import random

async def fetch_data(task_id):
    delay = random.randint(1, 5)  # Simulating a delay between 1 to 5 seconds
    print(f"Task {task_id}: Starting fetch (will take {delay} seconds)")
    await asyncio.sleep(delay)
    print(f"Task {task_id}: Finished fetching")
    return f"Data from task {task_id}"

async def process_data(task_id, data):
    print(f"Task {task_id}: Processing data: {data}")
    await asyncio.sleep(2)  # Simulate processing time
    print(f"Task {task_id}: Finished processing")

async def main():
    # Simulating 5 concurrent tasks
    tasks = [fetch_data(i) for i in range(1,6)]
    # tasks = []
    # for i in range(1, 6):
    #     tasks.append(fetch_data(i))

    # Fetch data concurrently
    results = await asyncio.gather(*tasks)

    # Process each fetched result

    process_tasks = [process_data(i, result) for i,result in enumerate(results)]
    #process_tasks = []
    # for i, result in enumerate(results):
    #     task = process_data((i+1), result)
    #     process_tasks.append(task)

    await asyncio.gather(*process_tasks)

asyncio.run(main())
