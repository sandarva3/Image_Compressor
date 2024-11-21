from django.shortcuts import render, redirect
from PIL import Image
from django.core.files.storage import FileSystemStorage
from io import BytesIO
import os
from os.path import getsize
from django.http import FileResponse, JsonResponse, HttpResponse, StreamingHttpResponse
from django.conf import settings


def calculate_quality(user_input):
    return int((100 - user_input) * 0.9 + 10)

def imageapp_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        compression_percentage = int(request.POST.get('compression_percentage'))


        quality = calculate_quality(compression_percentage)

        # Reading image using PIL
        img = Image.open(uploaded_file)

        # Compression
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)


        file_storage = FileSystemStorage()
        file_path = file_storage.save('compressed_' + uploaded_file.name, buffer)

        # response = FileResponse(open(file_path, 'rb'), content_type="image/jpeg")


        compressed_file_path = os.path.join(file_storage.location, file_path)
        compressed_file_size = getsize(compressed_file_path)
        rounded_size = round((compressed_file_size/1024), 2)

        print(f"File Storage Location is: {file_storage.location}")
        print(f"File path is :{file_path}")
        print(f"Compressed file path is : {compressed_file_path}")
        print(f"Compressed file size is: {rounded_size}")


        return JsonResponse({
            'status':'success',
            'filesize': rounded_size,
            'filename': file_path
        })

    return render(request, 'imageapp/image.html')

def download_view(request):
    if request.method == "GET":
        filename = request.GET.get('filename')

        try:
            file_path = os.path.join(settings.BASE_DIR, 'media', filename)
            print(f"FILE PATH IS : {file_path}")
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
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response

        except Exception as e:
            print(f"Something went Wrong. Exception: {e}")
            return HttpResponse("Something Went Wrong. EXCEPTION !")

    return HttpResponse('Something went wrong!')
