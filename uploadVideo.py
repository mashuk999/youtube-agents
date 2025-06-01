import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
import globalConfigs
import updateJson

cloudinary.config(
  cloud_name = 'indiajanega',
  api_key = globalConfigs.CLOUDINARY_API_KEY,
  api_secret = globalConfigs.CLOUDINARY_SECRET_KEY
)

upload_data = cloudinary.uploader.upload_large("output_video.mp4", 
  resource_type = "video",
  chunk_size = 6000000)

videoUrl=str(upload_data['secure_url'])

updateJson.update_placeholder_url(videoUrl)