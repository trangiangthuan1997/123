"""
Enhanced Image API with Bing + Google Images Scraper for maximum accuracy
"""
import requests
import time
import json
import base64
from typing import List, Dict, Optional
from dataclasses import dataclass
from urllib.parse import quote


@dataclass
class ImageResult:
    """Represents an image search result"""
    url: str
    download_url: str
    thumbnail_url: str
    source: str
    width: int
    height: int
    description: Optional[str] = None


class BingImageSearchAPI:
    """Bing Image Search API - Most accurate and powerful"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.bing.microsoft.com/v7.0/images/search"
        self.rate_limit_remaining = None

    def search_images(self, query: str, per_page: int = 10) -> List[ImageResult]:
        """Search for images using Bing Image Search API"""
        if not self.api_key:
            return []

        try:
            headers = {"Ocp-Apim-Subscription-Key": self.api_key}
            params = {
                "q": query,
                "count": min(per_page, 150),  # Bing max is 150
                "imageType": "Photo",
                "size": "Medium",  # Or Large
                "aspect": "All",
                "safeSearch": "Moderate"
            }

            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                results = []

                for item in data.get("value", [])[:per_page]:
                    results.append(ImageResult(
                        url=item["contentUrl"],
                        download_url=item["contentUrl"],
                        thumbnail_url=item["thumbnailUrl"],
                        source="Bing",
                        width=item.get("width", 800),
                        height=item.get("height", 600),
                        description=item.get("name")
                    ))

                print(f"[Bing] Found {len(results)} images for '{query}'")
                return results
            else:
                print(f"Bing API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Error searching Bing: {e}")
            return []

    def get_rate_limit_status(self) -> Optional[int]:
        return self.rate_limit_remaining


class GoogleImagesScraperAPI:
    """Google Images Web Scraper - Unlimited and FREE!"""

    def __init__(self):
        self.base_url = "https://www.google.com/search"

    def search_images(self, query: str, per_page: int = 10) -> List[ImageResult]:
        """Scrape images from Google Images"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            }

            params = {
                "q": query,
                "tbm": "isch",  # Image search
                "ijn": "0"
            }

            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"Google Images: HTTP {response.status_code}")
                return []

            # Extract image URLs from HTML
            results = []

            # Google Images data is in JSON format embedded in script tags
            # Look for AF_initDataCallback with image data
            import re

            # Find all image data
            matches = re.findall(r'\["(https://[^"]+?\.(?:jpg|jpeg|png|webp))"', response.text)

            # Also try to find from data attributes
            if not matches:
                matches = re.findall(r'data-src="([^"]+?\.(?:jpg|jpeg|png))"', response.text)

            # Filter and create results
            seen_urls = set()
            for url in matches[:per_page * 3]:  # Get more to filter
                # Skip duplicates
                if url in seen_urls:
                    continue

                # Skip small thumbnails
                if 'encrypted-tbn' in url or 's=' in url:
                    continue

                seen_urls.add(url)

                results.append(ImageResult(
                    url=url,
                    download_url=url,
                    thumbnail_url=url,
                    source="Google Images",
                    width=800,
                    height=600,
                    description=query
                ))

                if len(results) >= per_page:
                    break

            print(f"[Google Images] Found {len(results)} images for '{query}'")
            return results

        except Exception as e:
            print(f"Error scraping Google Images: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_rate_limit_status(self) -> Optional[int]:
        return None  # Unlimited


class UnsplashAPI:
    """Unsplash API - High quality photos"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.unsplash.com"
        self.headers = {"Authorization": f"Client-ID {api_key}"}
        self.rate_limit_remaining = None

    def search_images(self, query: str, per_page: int = 10) -> List[ImageResult]:
        """Search for images on Unsplash"""
        if not self.api_key:
            return []

        try:
            url = f"{self.base_url}/search/photos"
            params = {
                "query": query,
                "per_page": min(per_page, 30),
                "orientation": "landscape",
                "content_filter": "high"
            }

            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            if "X-Ratelimit-Remaining" in response.headers:
                self.rate_limit_remaining = int(response.headers["X-Ratelimit-Remaining"])

            if response.status_code == 200:
                data = response.json()
                results = []

                for photo in data.get("results", [])[:per_page]:
                    results.append(ImageResult(
                        url=photo["urls"]["regular"],
                        download_url=photo["urls"]["regular"],
                        thumbnail_url=photo["urls"]["thumb"],
                        source="Unsplash",
                        width=photo["width"],
                        height=photo["height"],
                        description=photo.get("description") or photo.get("alt_description")
                    ))

                return results
            else:
                print(f"Unsplash API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Error searching Unsplash: {e}")
            return []

    def get_rate_limit_status(self) -> Optional[int]:
        return self.rate_limit_remaining


class PexelsAPI:
    """Pexels API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1"
        self.headers = {"Authorization": api_key}
        self.rate_limit_remaining = None

    def search_images(self, query: str, per_page: int = 10) -> List[ImageResult]:
        """Search for images on Pexels"""
        if not self.api_key:
            return []

        try:
            url = f"{self.base_url}/search"
            params = {
                "query": query,
                "per_page": min(per_page, 80),
                "orientation": "landscape"
            }

            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            if "X-Ratelimit-Remaining" in response.headers:
                self.rate_limit_remaining = int(response.headers["X-Ratelimit-Remaining"])

            if response.status_code == 200:
                data = response.json()
                results = []

                for photo in data.get("photos", [])[:per_page]:
                    results.append(ImageResult(
                        url=photo["src"]["large"],
                        download_url=photo["src"]["large"],
                        thumbnail_url=photo["src"]["small"],
                        source="Pexels",
                        width=photo["width"],
                        height=photo["height"],
                        description=photo.get("alt")
                    ))

                return results
            else:
                print(f"Pexels API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Error searching Pexels: {e}")
            return []

    def get_rate_limit_status(self) -> Optional[int]:
        return self.rate_limit_remaining


class PixabayAPI:
    """Pixabay API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://pixabay.com/api/"
        self.rate_limit_remaining = None

    def search_images(self, query: str, per_page: int = 10) -> List[ImageResult]:
        """Search for images on Pixabay"""
        if not self.api_key:
            return []

        try:
            params = {
                "key": self.api_key,
                "q": query,
                "per_page": min(per_page, 200),
                "image_type": "photo",
                "orientation": "horizontal",
                "safesearch": "true",
                "editors_choice": "true"
            }

            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                results = []

                for photo in data.get("hits", [])[:per_page]:
                    results.append(ImageResult(
                        url=photo["largeImageURL"],
                        download_url=photo["largeImageURL"],
                        thumbnail_url=photo["previewURL"],
                        source="Pixabay",
                        width=photo["imageWidth"],
                        height=photo["imageHeight"],
                        description=photo.get("tags")
                    ))

                return results
            else:
                print(f"Pixabay API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Error searching Pixabay: {e}")
            return []

    def get_rate_limit_status(self) -> Optional[int]:
        return self.rate_limit_remaining


class EnhancedImageSearchManager:
    """Enhanced search manager with smart query variations and multiple sources"""

    def __init__(self, bing_key: str = "", unsplash_key: str = "", pexels_key: str = "", pixabay_key: str = ""):
        self.bing = BingImageSearchAPI(bing_key) if bing_key else None
        self.google_images = GoogleImagesScraperAPI()  # Always available!
        self.unsplash = UnsplashAPI(unsplash_key) if unsplash_key else None
        self.pexels = PexelsAPI(pexels_key) if pexels_key else None
        self.pixabay = PixabayAPI(pixabay_key) if pixabay_key else None

    def generate_query_variations(self, query: str) -> List[str]:
        """Generate multiple query variations for better results"""
        # KEEP IT SIMPLE - don't add negative keywords to queries
        # Filtering will happen AFTER we get results
        variations = [
            query,  # Original
            f"{query} object",
            f"{query} thing",
            f"{query} photo",
            f"{query} image"
        ]

        # Remove duplicates while preserving order
        seen = set()
        unique_variations = []
        for v in variations:
            if v.lower() not in seen:
                seen.add(v.lower())
                unique_variations.append(v)

        return unique_variations

    def is_unwanted_image(self, result: ImageResult) -> bool:
        """
        NEW APPROACH: Filter by IMAGE DIMENSIONS and ASPECT RATIO
        Instead of text patterns (which don't work well), we filter by image properties
        """
        width = result.width
        height = result.height
        url_lower = result.download_url.lower()

        # 1. BLOCK TOO SMALL IMAGES (icons, thumbnails, text images)
        # Text images and icons are usually small
        if width < 200 or height < 200:
            print(f"  ✗ BLOCKED: Too small ({width}x{height}) - likely icon/text/thumbnail")
            return True

        # 2. BLOCK EXTREME ASPECT RATIOS
        # Product photos are often in weird aspect ratios (tall/wide banners)
        aspect_ratio = width / height if height > 0 else 0

        # Too wide (banners, product listings)
        if aspect_ratio > 3.0:
            print(f"  ✗ BLOCKED: Too wide ({width}x{height}, ratio {aspect_ratio:.2f}) - likely banner/product listing")
            return True

        # Too tall (vertical banners, phone screenshots)
        if aspect_ratio < 0.4:
            print(f"  ✗ BLOCKED: Too tall ({width}x{height}, ratio {aspect_ratio:.2f}) - likely banner/screenshot")
            return True

        # 3. BLOCK KNOWN BAD DOMAINS (minimal list)
        bad_domains = [
            'amazon.com', 'ebay.com', 'aliexpress.com', 'walmart.com',
            'shutterstock.com', 'istockphoto.com', 'dreamstime.com',
            'definition', 'dictionary', 'meaning', 'vocabulary.com'
        ]

        for domain in bad_domains:
            if domain in url_lower:
                print(f"  ✗ BLOCKED: Bad domain ({domain})")
                return True

        # 4. BLOCK VECTOR FORMATS
        if url_lower.endswith(('.svg', '.ai', '.eps', '.pdf')):
            print(f"  ✗ BLOCKED: Vector file format")
            return True

        # Image passed all checks!
        print(f"  ✓ ACCEPTED: {width}x{height} (ratio {aspect_ratio:.2f})")
        return False

    def search_images(self, query: str, num_images: int = 6) -> List[ImageResult]:
        """
        NEW APPROACH: Prioritize SAFE sources first, fetch 10x more
        Priority: Unsplash > Pexels > Pixabay > Google Images > Bing
        """
        print(f"\n{'='*60}")
        print(f"[EnhancedSearch] Searching for '{query}', need {num_images} images")
        print(f"{'='*60}")

        all_results = []

        # Generate query variations
        query_variations = self.generate_query_variations(query)
        print(f"[EnhancedSearch] Query variations: {query_variations}")

        # NEW PRIORITY: SAFE SOURCES FIRST (Unsplash/Pexels/Pixabay)
        # These sources have high-quality photos without ads/text
        sources = []

        # Tier 1: Premium photo sites (SAFEST - try these first!)
        if self.unsplash:
            sources.append(("Unsplash", self.unsplash, 15))
        if self.pexels:
            sources.append(("Pexels", self.pexels, 15))
        if self.pixabay:
            sources.append(("Pixabay", self.pixabay, 15))

        # Tier 2: Web scrapers (good but need filtering)
        sources.append(("Google Images", self.google_images, 20))
        if self.bing:
            sources.append(("Bing", self.bing, 20))

        # Fetch 10x what we need to ensure quality after filtering
        target_fetch = num_images * 10

        # Try each source with query variations
        for source_name, source_obj, fetch_count in sources:
            if len(all_results) >= target_fetch:
                break

            print(f"\n[{source_name}] Starting search...")

            # Try MORE query variations for safe sources
            num_variations = 3 if source_name in ["Unsplash", "Pexels", "Pixabay"] else 2

            for variation in query_variations[:num_variations]:
                if len(all_results) >= target_fetch:
                    break

                try:
                    print(f"[{source_name}] Trying query: '{variation}'")
                    results = source_obj.search_images(variation, fetch_count)

                    if results:
                        # Filter unwanted images
                        print(f"[{source_name}] Filtering {len(results)} results...")
                        filtered_results = []
                        for r in results:
                            if not self.is_unwanted_image(r):
                                filtered_results.append(r)

                        print(f"[{source_name}] ✓ Kept {len(filtered_results)}/{len(results)} images after filtering")

                        # Add only new images (check for duplicates)
                        existing_urls = {r.download_url for r in all_results}
                        new_results = [r for r in filtered_results if r.download_url not in existing_urls]

                        if new_results:
                            all_results.extend(new_results)
                            print(f"[{source_name}] ✓ Added {len(new_results)} NEW clean images (total: {len(all_results)})")
                        else:
                            print(f"[{source_name}] ✗ All filtered images were duplicates")
                    else:
                        print(f"[{source_name}] ✗ No results")

                    time.sleep(0.3)  # Rate limiting

                except Exception as e:
                    print(f"[{source_name}] ERROR: {e}")
                    continue

            # DON'T stop early - keep fetching to get variety
            if len(all_results) >= num_images:
                print(f"[EnhancedSearch] ✓ Have {len(all_results)} images (need {num_images}), continuing for variety...")

        print(f"\n{'='*60}")
        print(f"[EnhancedSearch] FINAL: {len(all_results)} images found (needed {num_images})")
        print(f"{'='*60}\n")

        # Return first N images (we have plenty now!)
        return all_results[:num_images]

    def get_api_status(self) -> Dict[str, any]:
        """Get API rate limit status"""
        status = {}

        if self.bing:
            status["Bing"] = self.bing.get_rate_limit_status() or "Connected"

        status["Google Images"] = "Unlimited (Web Scraper)"

        if self.unsplash:
            status["Unsplash"] = self.unsplash.get_rate_limit_status()
        if self.pexels:
            status["Pexels"] = self.pexels.get_rate_limit_status()
        if self.pixabay:
            status["Pixabay"] = self.pixabay.get_rate_limit_status()

        return status


# For backward compatibility
ImageSearchManager = EnhancedImageSearchManager
