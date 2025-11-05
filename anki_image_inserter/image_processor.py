"""
Image processing and storage for Anki cards
"""
import io
import os
import requests
from typing import List, Optional
from PIL import Image
from .image_api import ImageResult


class ImageProcessor:
    """Handles image downloading, compression, and storage"""

    def __init__(self, max_width: int = 800, max_height: int = 600, quality: int = 85):
        self.max_width = max_width
        self.max_height = max_height
        self.quality = quality

    def download_image(self, url: str, timeout: int = 10) -> Optional[bytes]:
        """Download image from URL"""
        try:
            response = requests.get(url, timeout=timeout, stream=True)
            if response.status_code == 200:
                return response.content
            else:
                print(f"Failed to download image: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None

    def compress_image(self, image_data: bytes) -> Optional[bytes]:
        """Compress and resize image"""
        try:
            # Open image
            img = Image.open(io.BytesIO(image_data))

            # Convert to RGB if necessary (for PNG with transparency, etc.)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background

            # Resize if needed
            if img.width > self.max_width or img.height > self.max_height:
                img.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS)

            # Compress to JPEG
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=self.quality, optimize=True)
            return output.getvalue()

        except Exception as e:
            print(f"Error compressing image: {e}")
            return None

    def process_image(self, url: str) -> Optional[bytes]:
        """Download and process a single image"""
        image_data = self.download_image(url)
        if image_data:
            return self.compress_image(image_data)
        return None

    def process_images(self, image_results: List[ImageResult]) -> List[bytes]:
        """Process multiple images"""
        processed = []
        for result in image_results:
            image_data = self.process_image(result.download_url)
            if image_data:
                processed.append(image_data)
        return processed


class AnkiImageManager:
    """Manages image storage in Anki"""

    def __init__(self, collection):
        self.col = collection
        self.media = collection.media

    def add_images_to_media(self, images: List[bytes], prefix: str = "vocab_") -> List[str]:
        """Add images to Anki's media collection and return filenames"""
        filenames = []

        for i, image_data in enumerate(images):
            # Generate unique filename
            filename = f"{prefix}{hash(image_data)}_{i}.jpg"

            # Write to media folder
            try:
                self.media.write_data(filename, image_data)
                filenames.append(filename)
            except Exception as e:
                print(f"Error adding image to media: {e}")

        return filenames

    def format_images_html(self, filenames: List[str]) -> str:
        """Format image filenames as HTML for Anki field"""
        html_parts = []
        for filename in filenames:
            html_parts.append(f'<img src="{filename}">')

        return "<br>".join(html_parts)

    def clear_field_images(self, note, field_name: str):
        """Remove all images from a field"""
        if field_name in note:
            # Extract image filenames from HTML
            content = note[field_name]
            # Simple regex to find image sources
            import re
            image_files = re.findall(r'<img[^>]+src="([^"]+)"', content)

            # Delete from media collection
            for filename in image_files:
                try:
                    self.media.trash_files([filename])
                except Exception as e:
                    print(f"Error deleting image {filename}: {e}")

            # Clear the field
            note[field_name] = ""
