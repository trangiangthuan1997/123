"""
Image processing and storage for Anki cards
"""
import io
import os
import requests
from typing import List, Optional, Tuple
from PIL import Image
try:
    import imagehash
    IMAGEHASH_AVAILABLE = True
except ImportError:
    IMAGEHASH_AVAILABLE = False
    print("Warning: imagehash not available - duplicate detection disabled")
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
        """
        Process multiple images
        DEDUPLICATION DISABLED for SPEED - URL dedup already done in search
        """
        processed = []

        for result in image_results:
            image_data = self.process_image(result.download_url)
            if image_data:
                processed.append(image_data)

        print(f"\n[ImageProcessor] Processed {len(processed)}/{len(image_results)} images successfully")
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
        """
        Format image filenames as HTML for Anki field
        3-COLUMN RESPONSIVE GRID LAYOUT with auto-resize
        """
        if not filenames:
            return ""

        # CSS for responsive 3-column grid
        css = """
<style>
.vocab-images {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    width: 100%;
    max-width: 100%;
}

.vocab-images img {
    width: 100%;
    height: auto;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Responsive: 2 columns on tablets */
@media (max-width: 768px) {
    .vocab-images {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Responsive: 1 column on phones */
@media (max-width: 480px) {
    .vocab-images {
        grid-template-columns: 1fr;
    }
}
</style>
"""

        # Build HTML with grid container
        html_parts = [css, '<div class="vocab-images">']

        for filename in filenames:
            html_parts.append(f'<img src="{filename}" alt="vocabulary image">')

        html_parts.append('</div>')

        return "\n".join(html_parts)

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
