from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image
from io import BytesIO
import os



app = FastAPI()
MEDIA_ROOT = "/home/sandarva3/Desktop/projects/pencil/imageapp/async/media"
async def calculate_quality(user_input: int):
    return int((100 - user_input) * 0.9 + 10)



# to stream file
async def send_file(file_path):
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            yield chunk
    os.remove(file_path)



# Endpoint to handle file upload and compression
@app.post("/firstEndpoint/")
async def upload_img_view(image: UploadFile, compression_percentage: int = Form(...)):
    try:
        # Reading image using PIL
        img = Image.open(image.file)
        quality = await calculate_quality(compression_percentage)

        # Compress image and save to buffer
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)

        # Save to filesystem
        file_name = f"compressed_{image.filename}"
        file_path = os.path.join(MEDIA_ROOT, file_name)
        with open(file_path, "wb") as out_file:
            out_file.write(buffer.read())

        # Getting new file size
        file_size = os.path.getsize(file_path)
        file_size_kb = round(file_size / 1024, 2)

        return StreamingResponse(send_file(file_path), media_type="image/jpeg", headers={
            "Content-Disposition": f"attachment; filename={file_name}",
            "fileSize": str(file_size_kb)
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
