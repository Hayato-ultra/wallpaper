import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings
from typing import Optional

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_to_cloudinary(file_obj, folder='wallpapers', tags=None):
    result = cloudinary.uploader.upload(
        file_obj,
        folder=folder,
        tags=tags or [],
        resource_type='image',
        eager=[
            {'width': 500, 'height': 300, 'crop': 'thumb', 'gravity': 'auto'},
        ],
    )
    return result


def get_thumbnail_url(public_id: str) -> str:
    return cloudinary.CloudinaryImage(public_id).build_url(
        transformation=[
            {'width': 500, 'height': 300, 'crop': 'thumb', 'gravity': 'auto'},
            {'quality': 'auto', 'fetch_format': 'auto'},
        ]
    )


def get_blur_placeholder_url(public_id: str) -> str:
    return cloudinary.CloudinaryImage(public_id).build_url(
        transformation=[
            {'width': 50, 'quality': 'auto:low', 'effect': 'blur:1000'},
        ]
    )


def delete_from_cloudinary(public_id: str):
    return cloudinary.uploader.destroy(public_id)
