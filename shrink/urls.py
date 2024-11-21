from django.urls import path

from .views import (
    imageapp_view,
    download_view,
    uploadImg_view
    )

urlpatterns = [
    path('', imageapp_view, name='image'),
    path('download_compressed_image/', download_view, name="image_download"),
    path('uploadImg/', uploadImg_view),
]