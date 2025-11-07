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

    def generate_google_query_variations(self, query: str) -> List[str]:
        """
        BALANCED query variations for Google Images
        Mix of REAL PHOTOS and ILLUSTRATIONS for better diversity
        Priority: photo > illustration > wikipedia
        """
        variations = [
            query,                    # Original query - mixed results
            f"{query} photo",        # REAL PHOTOS priority
            f"{query} illustration", # Illustrations (less priority than before)
            f"{query} wikipedia",    # Wikipedia images are accurate
            f"{query} png",          # Transparent/quality format
            f"{query} clipart"       # Clipart last (minimal)
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
        BALANCED FILTERING: Block text/ads but not too strict
        Multi-layer filtering: size + ratio + URL patterns + description
        """
        width = result.width
        height = result.height
        url_lower = result.download_url.lower()
        desc_lower = (result.description or "").lower()

        # 1. BLOCK SMALL IMAGES (text images, icons, thumbnails)
        # 200px is balanced - not too strict, not too loose
        if width < 200 or height < 200:
            print(f"  ✗ BLOCKED: Too small ({width}x{height}) - likely text/icon/thumbnail")
            return True

        # 2. BLOCK EXTREME ASPECT RATIOS
        aspect_ratio = width / height if height > 0 else 0

        # Banners, product listings
        if aspect_ratio > 3.5:
            print(f"  ✗ BLOCKED: Too wide ({width}x{height}, ratio {aspect_ratio:.2f}) - likely banner/ad")
            return True

        # Vertical banners, screenshots
        if aspect_ratio < 0.3:
            print(f"  ✗ BLOCKED: Too tall ({width}x{height}, ratio {aspect_ratio:.2f}) - likely banner/screenshot")
            return True

        # 3. BLOCK KEY BAD SITES (simplified list - most important ones)
        bad_sites = [
            # E-commerce
            'amazon', 'ebay', 'aliexpress', 'walmart', 'etsy',
            'redbubble', 'zazzle', 'teespring',
            # Games
            'steam', 'epicgames', 'gamespot', 'ign.com',
            # Text/quotes
            'dictionary', 'vocabulary.com', 'quote', 'meme',
            # Stock with watermarks
            'shutterstock', 'istockphoto', 'dreamstime', 'gettyimages'
        ]
        for site in bad_sites:
            if site in url_lower:
                print(f"  ✗ BLOCKED: Bad site ({site})")
                return True

        # 4. BLOCK BAD URL PATHS
        bad_paths = [
            '/product/', '/item/', '/buy/', '/shop/', '/game/',
            '-product-', '-buy-', '-game-'
        ]
        for path in bad_paths:
            if path in url_lower:
                print(f"  ✗ BLOCKED: Bad URL path ({path})")
                return True

        # 5. BLOCK BAD DESCRIPTIONS (simplified)
        bad_descs = [
            # Text
            'definition', 'quote', 'typography', 'lettering',
            # Commerce
            'buy', 'sale', 'shop', 'discount',
            # Games
            'gameplay', 'game screenshot', 'video game',
            # Stock
            'stock photo', 'royalty free'
        ]
        for desc in bad_descs:
            if desc in desc_lower:
                print(f"  ✗ BLOCKED: Bad description ({desc})")
                return True

        # Image passed all checks!
        print(f"  ✓ ACCEPTED: {width}x{height} (ratio {aspect_ratio:.2f})")
        return False

    def search_images(self, query: str, num_images: int = 6) -> List[ImageResult]:
        """
        PRIORITY: Google Images (special queries) > Bing > Unsplash > Pexels > Pixabay
        Google gets SPECIAL queries for illustration/clipart/wikipedia
        """
        print(f"\n{'='*60}")
        print(f"[EnhancedSearch] Searching for '{query}', need {num_images} images")
        print(f"{'='*60}")

        all_results = []

        # Generate DIFFERENT query variations for different sources
        standard_variations = self.generate_query_variations(query)
        google_variations = self.generate_google_query_variations(query)

        print(f"[EnhancedSearch] Standard variations: {standard_variations[:2]}")
        print(f"[EnhancedSearch] Google variations: {google_variations[:3]}")

        # PRIORITY: Google FIRST with special queries for illustration/clipart!
        sources = []

        # Tier 1: Google Images with SPECIAL queries (HIGHEST PRIORITY!)
        sources.append(("Google Images", self.google_images, 20, google_variations, 3))

        # Tier 2: Bing with standard queries
        if self.bing:
            sources.append(("Bing", self.bing, 20, standard_variations, 2))

        # Tier 3: Premium photo sites with standard queries
        if self.unsplash:
            sources.append(("Unsplash", self.unsplash, 15, standard_variations, 2))
        if self.pexels:
            sources.append(("Pexels", self.pexels, 15, standard_variations, 2))
        if self.pixabay:
            sources.append(("Pixabay", self.pixabay, 15, standard_variations, 2))

        # Fetch 10x what we need (balanced approach)
        target_fetch = num_images * 10

        # Try each source with its specific query variations
        for source_info in sources:
            if len(all_results) >= target_fetch:
                break

            source_name = source_info[0]
            source_obj = source_info[1]
            fetch_count = source_info[2]
            variations = source_info[3]
            num_variations = source_info[4]

            print(f"\n[{source_name}] Starting search...")

            # Try N variations for this source
            for variation in variations[:num_variations]:
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

            # If we have enough, continue for variety (but stop after target_fetch)
            if len(all_results) >= num_images:
                print(f"[EnhancedSearch] ✓ Have {len(all_results)} images (need {num_images})")

        print(f"\n{'='*60}")
        print(f"[EnhancedSearch] FINAL: {len(all_results)} images found (needed {num_images})")

        if len(all_results) < num_images:
            print(f"⚠ WARNING: Only found {len(all_results)}/{num_images} images after filtering!")

        print(f"{'='*60}\n")

        # Return first N images (or all if less than N)
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
