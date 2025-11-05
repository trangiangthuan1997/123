"""
Image API clients for Unsplash, Pexels, and Pixabay
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
            url = f"{self.base_url}/search/photos"
            params = {
                "query": query,
                "per_page": per_page,
                "orientation": "landscape"
            }

            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            # Update rate limit info
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
        """Get remaining API requests"""
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
                "per_page": per_page,
                "orientation": "landscape"
            }

            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            # Update rate limit info
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
        """Get remaining API requests"""
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
                "per_page": per_page,
                "image_type": "photo",
                "orientation": "horizontal",
                "safesearch": "true"
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
        """Get remaining API requests"""
        return self.rate_limit_remaining


class ImageSearchManager:
    """Manages image searches across multiple sources"""

    def __init__(self, unsplash_key: str, pexels_key: str, pixabay_key: str):
        self.unsplash = UnsplashAPI(unsplash_key) if unsplash_key else None
        self.pexels = PexelsAPI(pexels_key) if pexels_key else None
        self.pixabay = PixabayAPI(pixabay_key) if pixabay_key else None

    def search_images(self, query: str, num_images: int = 6) -> List[ImageResult]:
        """Search for images across all available sources"""
        all_results = []
        images_per_source = max(2, num_images // 3)

        # Try Unsplash first
        if self.unsplash:
            try:
                results = self.unsplash.search_images(query, images_per_source)
                all_results.extend(results)
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"Unsplash search failed: {e}")

        # Try Pexels
        if self.pexels and len(all_results) < num_images:
            try:
                results = self.pexels.search_images(query, images_per_source)
                all_results.extend(results)
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"Pexels search failed: {e}")

        # Try Pixabay
        if self.pixabay and len(all_results) < num_images:
            try:
                results = self.pixabay.search_images(query, images_per_source)
                all_results.extend(results)
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"Pixabay search failed: {e}")

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

        return status
