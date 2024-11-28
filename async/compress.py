import os
import asyncio
import httpx

source = "/home/sandarva3/Pictures/check"
destination = "/home/sandarva3/Pictures/results"
count = 1

os.chdir(source)


# Async function to upload a file
async def upload(filePath, fileName, compressionAmount, counter):
    destinationPath = os.path.join(destination, fileName)
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        with open(filePath, 'rb') as file:
            response = await client.post(
                'http://127.0.0.1:8000/firstEndpoint/',
                files={'image': (fileName, file)},
                data={'compression_percentage': compressionAmount}
            )

        if response.status_code == 200:
            with open(destinationPath, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            print(f"File {counter} is Done.")
        else:
            print("There was an error. Please try again.")
            print(f"The whole response object: {response}")
            print(f"The response text: {response.text}")


async def fetchFile():
    global count
    uploaded_files = []
    for f in os.listdir():
        filePath = os.path.join(source, f)
        fileName = str(f)
        print(f"File no: {count}")
        uploaded_files.append(upload(filePath, fileName, 75, count))
        count += 1

    await asyncio.gather(*uploaded_files)


asyncio.run(fetchFile())
