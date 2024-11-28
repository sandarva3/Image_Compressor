import os
import asyncio
import httpx

source = "/home/sandarva3/Pictures/Chaurasi Photos"
destination = "/home/sandarva3/Pictures/compressedPhotos2"

os.chdir(source)


async def upload(filePath, fileName, compressionAmount, counter):
    destinationPath = os.path.join(destination, fileName)
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            with open(filePath, 'rb') as file:
                response = await client.post(
                    'http://127.0.0.1:8000/uploadImg/',
                    files={'image': (fileName, file)},
                    data={'compression_percentage': compressionAmount}
                )

        if response.status_code == 200:
            with open(destinationPath, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            print(f"File {counter} is Done.")
        else:
            print(f"Error for File {counter}: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"Failed to upload {fileName}: {e}")


async def process_in_batches(batch_size=25, delay=2):
    files = os.listdir()
    total_files = len(files)
    count = 1

    for i in range(0, total_files, batch_size):
        batch = files[i:i + batch_size]
        tasks = []

        for file_name in batch:
            file_path = os.path.join(source, file_name)
            print(f"Scheduling File {count}")
            tasks.append(upload(file_path, file_name, 75, count))
            count += 1

        await asyncio.gather(*tasks)

        # Pause between batches
        # if i + batch_size < total_files:  # Only pause if there are more batches
        #     print(f"PAUSING for {delay} seconds...")
        #     await asyncio.sleep(delay)


asyncio.run(process_in_batches(batch_size=25, delay=2))
