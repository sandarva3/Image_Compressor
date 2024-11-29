from django.shortcuts import render
from PIL import Image
from django.core.files.storage import FileSystemStorage
from io import BytesIO
import os
from os.path import getsize
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import asyncio
import json
#from asgiref.sync import sync_to_async


async def calculate_quality(user_input):
    return int((100 - user_input) * 0.9 + 10)


async def sendFile(filePath):
    with open(filePath, 'rb') as file:
        while True:
            data = file.read(8192)
            if not data:
                break
            yield data
    os.remove(filePath)


@csrf_exempt
async def uploadImg_view(request):
    if request.method == "POST":
        response_data = await imageapp_view(request)

        try:
            response = json.loads(response_data.content)
            fileName = response.get('filename')
            if not fileName:
                raise ValueError("Filename missing in response")

            filePath = os.path.join(settings.MEDIA_ROOT, fileName)

        
            responseClient = StreamingHttpResponse(sendFile(filePath), content_type="image/jpeg")
            responseClient['Content-Disposition'] = f"attachment; filename={fileName}"
            responseClient['fileName'] = fileName

            return responseClient
        except Exception as e:
            print(f"Error handling response: {e}")
            return HttpResponse("An error occurred while processing the response.", status=500)
    else:
        return HttpResponse("Not a POST request")


async def imageapp_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('image')
        if not uploaded_file:
            return JsonResponse({"error": "No image provided"}, status=400)

        try:
            compression_percentage = int(request.POST.get('compression_percentage', 50))
        except ValueError:
            return JsonResponse({"error": "Invalid compression percentage"}, status=400)

        quality = await calculate_quality(compression_percentage)

        try:
            # Reading image using PIL
            img = Image.open(uploaded_file)

            # Compression
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=quality)
            buffer.seek(0)

            file_storage = FileSystemStorage()
            file_name = f"compressed_{uploaded_file.name}"
            #file_path = await sync_to_async((file_storage.save))(file_name, buffer)
            file_path = (file_storage.save)(file_name, buffer)

            compressed_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            compressed_file_size = getsize(compressed_file_path)
            rounded_size = round((compressed_file_size / 1024), 2)

            return JsonResponse({
                'status': 'success',
                'filesize': rounded_size,
                'filename': file_name
            })
        except Exception as e:
            print(f"Error compressing file: {e}")
            return JsonResponse({"error": "An error occurred during compression."}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def download_view(request):
    if request.method == "GET":
        filename = request.GET.get('filename')

        try:
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            print(f"FILE PATH IS: {file_path}")

            # Generator function to read file in chunks
            def file_stream():
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(8192)  # 8KB at a time
                        if not data:
                            break
                        yield data
                os.remove(file_path)

            response = StreamingHttpResponse(file_stream(), content_type='image/jpeg')
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            return response

        except Exception as e:
            print(f"Something went wrong. Exception: {e}")
            return HttpResponse("Something went wrong. EXCEPTION!", status=500)

    return HttpResponse("Invalid request method", status=405)
