from photo_metadata_server import get_photo_metadata
import os

file_path = os.path.expanduser("~/pictures/post/DSC01630.JPG")
print(f"Testing metadata extraction for: {file_path}")
print(get_photo_metadata(file_path))
