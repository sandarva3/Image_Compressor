import os
import requests


def upload(filePath, compressionAmount):
    print(f"The file Path is: {filePath}")
    with open(filePath, 'rb') as file:
            response = requests.post(
            'http://127.0.0.1:8000/uploadImg/',
            files={'image': file},
            data = {'compression_percentage': compressionAmount}
            )

            if response.status_code == 200:
                print(f"File is successfully Compressed and received.")
                ContentDisposition = response.headers['Content-Disposition']
                print(f"The CONTENT-DISPOSITION IS: {ContentDisposition}")
                fileName = response.headers['fileName']
                print(f"The file Name is: {fileName}")
                
                with open(fileName, "wb") as f:
                    for chunk in response.iter_content(8192):
                        f.write(chunk)
                
                print(f"The Compressed file is saved as: {fileName}")

            else:
                 print("There was error. Please try again.")
                 print(f"The whole response object: {response}")
                 print(f"The response text: {response.text}")


upload("hello.jpg", 75)

