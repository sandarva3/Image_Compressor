import os
import requests
import asyncio



source = "/home/sandarva3/Pictures/check"
destination = "/home/sandarva3/Pictures/results"

# print("Writing in the Source folder.")
# with open(f"{source}/check.txt", 'w') as f:
#     f.write(f"HELLO WORLD, This is the source path: {source}")
#     print("Wrote in the Source folder.")


# with open(f"{destination}/check.txt", 'w') as f:
#     f.write(f"Checking, this is the destination path: {destination}")
#     print("Wrote in destination path")

count = 1




os.chdir(source)

'''
def upload(filePath, fileName, compressionAmount):
    destinationPath = os.path.join(destination, fileName)
    with open(filePath, 'rb') as file:

        response = requests.post(
        'http://127.0.0.1:8000/uploadImg/',
        files={'image': file},
        data = {'compression_percentage': compressionAmount}
        )

        if response.status_code == 200:               
            with open(destinationPath, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            print(f"File {count} is Done.")

        else:
             print("There was error. Please try again.")
             print(f"The whole response object: {response}")
             print(f"The response text: {response.text}")



for f in os.listdir():
    filePath = os.path.join(source, f)
    fileName = str(f)
    print(f"File no: {count}.")
    upload(filePath, fileName, 75)
    count += 1
'''

async def upload(filePath, fileName, compressionAmount, counter):
    destinationPath = os.path.join(destination, fileName)
    with open(filePath, 'rb') as file:

        response = requests.post(
        'http://127.0.0.1:8000/uploadImg/',
        files={'image': file},
        data = {'compression_percentage': compressionAmount}
        )

        if response.status_code == 200:               
            with open(destinationPath, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            print(f"File {counter} is Done.")

        else:
             print("There was error. Please try again.")
             print(f"The whole response object: {response}")
             print(f"The response text: {response.text}")

uploaded_files = []
async def fetchFile():
    global count
    for f in os.listdir():
        filePath = os.path.join(source, f)
        fileName = str(f)
        print(f"File no: {count}")
        uploaded_files.append(upload(filePath, fileName, 75, count))
        count += 1
    await asyncio.gather(*uploaded_files)

asyncio.run(fetchFile())