"""
Image API clients for multiple sources with improved accuracy
"""
import requests
import time
from typing import List, Dict, Optional
from dataclasses import dataclass


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


class UnsplashAPI:
    """Client for Unsplash API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.unsplash.com"
        self.headers = {"Authorization": f"Client-ID {api_key}"}
        self.rate_limit_remaining = None

    def search_images(self, query: str, per_page: int = 6) -> List[ImageResult]:
        """Search for images on Unsplash"""
        try:
            # Improve query for vocabulary words
            enhanced_query = f"{query} object thing"

            url = f"{self.base_url}/search/photos"
            params = {
                "query": enhanced_query,
                "per_page": min(per_page, 30),  # Unsplash max is 30
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
    """Client for Pexels API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1"
        self.headers = {"Authorization": api_key}
        self.rate_limit_remaining = None

    def search_images(self, query: str, per_page: int = 6) -> List[ImageResult]:
        """Search for images on Pexels"""
        try:
            url = f"{self.base_url}/search"
            params = {
                "query": query,
                "per_page": min(per_page, 80),  # Pexels max is 80
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
    """Client for Pixabay API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://pixabay.com/api/"
        self.rate_limit_remaining = None

    def search_images(self, query: str, per_page: int = 6) -> List[ImageResult]:
        """Search for images on Pixabay"""
        try:
            params = {
                "key": self.api_key,
                "q": query,
                "per_page": min(per_page, 200),  # Pixabay max is 200
                "image_type": "photo",
                "orientation": "horizontal",
                "safesearch": "true",
                "editors_choice": "true"  # Higher quality images
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


class GoogleCustomSearchAPI:
    """Client for Google Custom Search API"""

    def __init__(self, api_key: str, cx: str):
        self.api_key = api_key
        self.cx = cx  # Custom Search Engine ID
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.rate_limit_remaining = None

    def search_images(self, query: str, per_page: int = 6) -> List[ImageResult]:
        """Search for images using Google Custom Search"""
        try:
            # Google CSE returns max 10 results per request
            params = {
                "key": self.api_key,
                "cx": self.cx,
                "q": query,
                "searchType": "image",
                "num": min(per_page, 10),
                "imgSize": "large",
                "imgType": "photo",
                "safe": "active",
                "fileType": "jpg"
            }

            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                results = []

                for item in data.get("items", [])[:per_page]:
                    image_data = item.get("image", {})
                    results.append(ImageResult(
                        url=item["link"],
                        download_url=item["link"],
                        thumbnail_url=image_data.get("thumbnailLink", item["link"]),
                        source="Google",
                        width=image_data.get("width", 800),
                        height=image_data.get("height", 600),
                        description=item.get("title")
                    ))

                return results
            else:
                print(f"Google CSE API error: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            print(f"Error searching Google: {e}")
            return []

    def get_rate_limit_status(self) -> Optional[int]:
        return self.rate_limit_remaining


class DuckDuckGoImageSearch:
    """Client for DuckDuckGo image search (no API key required)"""

    def __init__(self):
        self.base_url = "https://duckduckgo.com"

    def search_images(self, query: str, per_page: int = 6) -> List[ImageResult]:
        """Search for images using DuckDuckGo"""
        try:
            # Get search token
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })

            # Get vqd token with shorter timeout
            params = {"q": query}
            response = session.get(f"{self.base_url}/", params=params, timeout=5)

            # Extract vqd token from response
            import re
            vqd_match = re.search(r'vqd=[\'"]([\d-]+)[\'"]', response.text)
            if not vqd_match:
                print("DuckDuckGo: Could not find vqd token")
                return []

            vqd = vqd_match.group(1)

            # Search for images with shorter timeout
            params = {
                "l": "us-en",
                "o": "json",
                "q": query,
                "vqd": vqd,
                "f": ",,,",
                "p": "1",
                "v7exp": "a"
            }

            response = session.get(
                f"{self.base_url}/i.js",
                params=params,
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                results = []

                for item in data.get("results", [])[:per_page]:
                    results.append(ImageResult(
                        url=item["image"],
                        download_url=item["image"],
                        thumbnail_url=item.get("thumbnail", item["image"]),
                        source="DuckDuckGo",
                        width=item.get("width", 800),
                        height=item.get("height", 600),
                        description=item.get("title")
                    ))

                return results
            else:
                print(f"DuckDuckGo search error: {response.status_code}")
                return []

        except requests.exceptions.Timeout:
            print(f"DuckDuckGo: Timeout error (network too slow or blocked)")
            return []
        except requests.exceptions.ConnectionError:
            print(f"DuckDuckGo: Connection error (may be blocked)")
            return []
        except Exception as e:
            print(f"DuckDuckGo: Unexpected error: {e}")
            return []

    def get_rate_limit_status(self) -> Optional[int]:
        return None  # No rate limit for DuckDuckGo


class ImageSearchManager:
    """Manages image searches across multiple sources with improved accuracy"""

    def __init__(self, unsplash_key: str = "", pexels_key: str = "",
                 pixabay_key: str = "", google_key: str = "", google_cx: str = ""):
        self.unsplash = UnsplashAPI(unsplash_key) if unsplash_key else None
        self.pexels = PexelsAPI(pexels_key) if pexels_key else None
        self.pixabay = PixabayAPI(pixabay_key) if pixabay_key else None
        self.google = GoogleCustomSearchAPI(google_key, google_cx) if (google_key and google_cx) else None
        self.duckduckgo = DuckDuckGoImageSearch()

    def search_images(self, query: str, num_images: int = 6) -> List[ImageResult]:
        """Search for images across all available sources with fallback"""
        print(f"[ImageSearch] Searching for '{query}', need {num_images} images")
        all_results = []

        # Priority order: Google > Unsplash > Pexels > Pixabay
        # DuckDuckGo only used as last resort if others fail
        primary_sources = []

        if self.google:
            primary_sources.append(("Google", self.google, 3))
        if self.unsplash:
            primary_sources.append(("Unsplash", self.unsplash, 2))
        if self.pexels:
            primary_sources.append(("Pexels", self.pexels, 2))
        if self.pixabay:
            primary_sources.append(("Pixabay", self.pixabay, 2))

        # Try each primary source
        for source_name, source_obj, images_per_source in primary_sources:
            if len(all_results) >= num_images:
                break

            try:
                remaining_needed = num_images - len(all_results)
                to_fetch = min(images_per_source, remaining_needed)

                print(f"[ImageSearch] Trying {source_name} for {to_fetch} images...")
                results = source_obj.search_images(query, to_fetch)

                if results:
                    all_results.extend(results)
                    print(f"[ImageSearch] Got {len(results)} images from {source_name}")
                else:
                    print(f"[ImageSearch] No results from {source_name}")

                time.sleep(0.2)  # Rate limiting

            except Exception as e:
                print(f"[ImageSearch] {source_name} search failed: {e}")
                continue

        # If still not enough, try secondary search from primary sources
        if len(all_results) < num_images and len(primary_sources) > 0:
            print(f"[ImageSearch] Only got {len(all_results)} images, trying secondary search from primary sources...")

            for source_name, source_obj, _ in primary_sources:
                if len(all_results) >= num_images:
                    break

                try:
                    remaining = num_images - len(all_results)
                    results = source_obj.search_images(query, remaining)

                    # Add only new images
                    existing_urls = {r.download_url for r in all_results}
                    new_results = [r for r in results if r.download_url not in existing_urls]

                    if new_results:
                        all_results.extend(new_results)
                        print(f"[ImageSearch] Got {len(new_results)} more images from {source_name}")

                    time.sleep(0.2)

                except Exception as e:
                    print(f"[ImageSearch] Secondary {source_name} search failed: {e}")
                    continue

        # Last resort: Try DuckDuckGo only if still not enough images
        if len(all_results) < num_images:
            try:
                remaining = num_images - len(all_results)
                print(f"[ImageSearch] Still need {remaining} images, trying DuckDuckGo as last resort...")

                ddg_results = self.duckduckgo.search_images(query, remaining)

                if ddg_results:
                    # Add only new images
                    existing_urls = {r.download_url for r in all_results}
                    new_results = [r for r in ddg_results if r.download_url not in existing_urls]

                    if new_results:
                        all_results.extend(new_results)
                        print(f"[ImageSearch] Got {len(new_results)} images from DuckDuckGo")
                else:
                    print(f"[ImageSearch] DuckDuckGo returned no results")

            except Exception as e:
                print(f"[ImageSearch] DuckDuckGo failed (skipping): {e}")

        print(f"[ImageSearch] Total images found: {len(all_results)}")
        return all_results[:num_images]

    def get_api_status(self) -> Dict[str, Optional[int]]:
        """Get API rate limit status for all services"""
        status = {}

        if self.unsplash:
            status["Unsplash"] = self.unsplash.get_rate_limit_status()
        if self.pexels:
            status["Pexels"] = self.pexels.get_rate_limit_status()
        if self.pixabay:
            status["Pixabay"] = self.pixabay.get_rate_limit_status()
        if self.google:
            status["Google"] = self.google.get_rate_limit_status()

        # DuckDuckGo as fallback only (no status check to avoid timeout)
        status["DuckDuckGo"] = "Fallback only (no API key needed)"

        return status
