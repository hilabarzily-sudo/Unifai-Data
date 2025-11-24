"""
Universal Civitai Content Downloader
Downloads EVERYTHING: images, videos, articles, posts, prompts
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm
import pandas as pd
from config import API_CONFIG, USER_AGENT
import re
from urllib.parse import urlparse


class UniversalCivitaiDownloader:
    """Downloads ALL content types from Civitai models"""

    def __init__(self, output_dir: str = "./all_content"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.api_key = API_CONFIG["api_key"]
        self.base_url = API_CONFIG["base_url"]
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Authorization": f"Bearer {self.api_key}"
        })

        # Statistics
        self.stats = {
            "models_processed": 0,
            "images_downloaded": 0,
            "videos_downloaded": 0,
            "articles_found": 0,
            "posts_downloaded": 0,
            "prompts_saved": 0,
            "total_size_mb": 0,
            "errors": 0
        }

    def sanitize_filename(self, name: str) -> str:
        """Clean filename for filesystem"""
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        name = re.sub(r'[^\x00-\x7F]+', '_', name)
        return name[:100].strip()

    def get_model_full_data(self, model_id: int) -> Optional[Dict]:
        """Fetch ALL data for a model including posts and articles"""
        try:
            response = self.session.get(
                f"{self.base_url}/models/{model_id}",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching model {model_id}: {e}")
            return None

    def get_model_posts(self, model_id: int) -> List[Dict]:
        """Fetch all posts/community content for a model"""
        try:
            # Try to get posts via API (if available)
            # Note: This might need adjustment based on actual API endpoints
            posts = []

            # For now, we'll extract posts from model data
            model_data = self.get_model_full_data(model_id)
            if model_data:
                # Check for community/post data in model
                for version in model_data.get("modelVersions", []):
                    if "posts" in version:
                        posts.extend(version["posts"])

            return posts
        except Exception as e:
            print(f"Error fetching posts for {model_id}: {e}")
            return []

    def download_file(self, url: str, save_path: Path, file_type: str = "file") -> bool:
        """Download any file (image/video/etc)"""
        try:
            response = self.session.get(url, timeout=60, stream=True)
            response.raise_for_status()

            # Get file size
            total_size = int(response.headers.get('content-length', 0))

            with open(save_path, 'wb') as f:
                if total_size > 0:
                    # Show progress for large files (videos)
                    with tqdm(total=total_size, unit='B', unit_scale=True,
                             desc=f"  {file_type}", leave=False) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                            pbar.update(len(chunk))
                else:
                    # No progress bar for unknown size
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

            # Track size
            size_mb = save_path.stat().st_size / (1024 * 1024)
            self.stats["total_size_mb"] += size_mb

            return True

        except Exception as e:
            print(f"Error downloading {file_type}: {e}")
            return False

    def extract_all_metadata(self, content_data: Dict) -> Dict:
        """Extract ALL metadata including prompts from any content"""
        metadata = {
            "prompt": "",
            "negative_prompt": "",
            "steps": None,
            "sampler": None,
            "cfg_scale": None,
            "seed": None,
            "model": None,
            "width": content_data.get("width"),
            "height": content_data.get("height"),
            "nsfw": content_data.get("nsfw"),
            "url": content_data.get("url"),
            "type": content_data.get("type", "image"),
            "has_prompt": False,
        }

        # Extract from meta field
        meta = content_data.get("meta", {})
        if meta:
            metadata["prompt"] = meta.get("prompt", "")
            metadata["negative_prompt"] = meta.get("negativePrompt", "")
            metadata["steps"] = meta.get("steps")
            metadata["sampler"] = meta.get("sampler")
            metadata["cfg_scale"] = meta.get("cfgScale")
            metadata["seed"] = meta.get("seed")
            metadata["model"] = meta.get("Model")

            # Check if has actual prompt
            if metadata["prompt"]:
                metadata["has_prompt"] = True

        return metadata

    def save_content_metadata(self, metadata: Dict, save_path: Path):
        """Save metadata to text file"""
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                if metadata["prompt"]:
                    f.write("=== PROMPT ===\n")
                    f.write(metadata["prompt"] + "\n\n")

                if metadata["negative_prompt"]:
                    f.write("=== NEGATIVE PROMPT ===\n")
                    f.write(metadata["negative_prompt"] + "\n\n")

                f.write("=== SETTINGS ===\n")
                f.write(f"Type: {metadata.get('type', 'unknown')}\n")
                f.write(f"Steps: {metadata['steps']}\n")
                f.write(f"Sampler: {metadata['sampler']}\n")
                f.write(f"CFG Scale: {metadata['cfg_scale']}\n")
                f.write(f"Seed: {metadata['seed']}\n")
                f.write(f"Model: {metadata['model']}\n")

                if metadata.get('width') and metadata.get('height'):
                    f.write(f"Size: {metadata['width']}x{metadata['height']}\n")

                if metadata.get('url'):
                    f.write(f"\nOriginal URL: {metadata['url']}\n")

        except Exception as e:
            print(f"Error saving metadata: {e}")

    def download_model_all_content(self, model_data: Dict,
                                   max_items: Optional[int] = None,
                                   download_videos: bool = True,
                                   download_images: bool = True):
        """Download ALL content for a single model"""
        model_id = model_data.get("model_id")
        model_name = model_data.get("model_name", f"model_{model_id}")

        # Create model directory structure
        safe_name = self.sanitize_filename(model_name)
        model_dir = self.output_dir / safe_name

        # Subdirectories for different content types
        images_dir = model_dir / "images"
        videos_dir = model_dir / "videos"
        prompts_dir = model_dir / "prompts"
        articles_dir = model_dir / "articles"

        for d in [images_dir, videos_dir, prompts_dir, articles_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # Get full model data
        full_data = self.get_model_full_data(model_id)
        if not full_data:
            print(f"No data found for {model_name}")
            return

        # Collect ALL content items
        all_content = []

        for version in full_data.get("modelVersions", []):
            version_name = version.get("name", "unknown")

            # Get images and videos from this version
            for item in version.get("images", []):
                item["version_name"] = version_name
                item["version_id"] = version.get("id")
                all_content.append(item)

        # Limit if specified
        if max_items:
            all_content = all_content[:max_items]

        if not all_content:
            print(f"No content found for {model_name}")
            return

        print(f"\n📥 Downloading content from: {model_name}")
        print(f"   Found: {len(all_content)} items")

        # Save model info with article/description
        model_info = {
            "model_id": model_id,
            "model_name": model_name,
            "model_url": model_data.get("model_url"),
            "type": model_data.get("type"),
            "downloads": model_data.get("downloads"),
            "creator": model_data.get("creator_username"),
            "base_model": model_data.get("base_model"),
            "description": full_data.get("description", ""),
            "tags": full_data.get("tags", []),
            "total_content_items": len(all_content),
        }

        # Save model info
        with open(model_dir / "model_info.json", 'w', encoding='utf-8') as f:
            json.dump(model_info, f, indent=2, ensure_ascii=False)

        # Save description as article if exists
        if model_info.get("description"):
            article_path = articles_dir / "model_description.txt"
            with open(article_path, 'w', encoding='utf-8') as f:
                f.write(f"# {model_name}\n\n")
                f.write(model_info["description"])
            self.stats["articles_found"] += 1

        # Download each content item
        items_with_prompts = 0

        for idx, content in enumerate(tqdm(all_content, desc=f"  {model_name[:40]}")):
            content_id = content.get("id", idx)
            content_url = content.get("url")
            content_type = content.get("type", "image")

            if not content_url:
                continue

            # Determine file type and extension
            url_lower = content_url.lower()
            is_video = any(ext in url_lower for ext in ['.mp4', '.webm', '.mov', 'video'])

            if is_video and not download_videos:
                continue
            if not is_video and not download_images:
                continue

            # Determine extension
            if is_video:
                ext = "mp4"
                if ".webm" in url_lower:
                    ext = "webm"
                content_category = "video"
            else:
                ext = "png"
                if "jpeg" in url_lower or "jpg" in url_lower:
                    ext = "jpg"
                elif "webp" in url_lower:
                    ext = "webp"
                content_category = "image"

            # File paths
            if is_video:
                content_dir = videos_dir
            else:
                content_dir = images_dir

            content_filename = f"{content_category}_{idx+1:03d}_{content_id}.{ext}"
            prompt_filename = f"{content_category}_{idx+1:03d}_{content_id}_prompt.txt"
            metadata_filename = f"{content_category}_{idx+1:03d}_{content_id}_metadata.json"

            content_path = content_dir / content_filename
            prompt_path = prompts_dir / prompt_filename
            metadata_path = prompts_dir / metadata_filename

            # Skip if already downloaded
            if content_path.exists():
                continue

            # Download content
            file_type = "video" if is_video else "image"
            if self.download_file(content_url, content_path, file_type):
                if is_video:
                    self.stats["videos_downloaded"] += 1
                else:
                    self.stats["images_downloaded"] += 1

                # Extract and save metadata
                metadata = self.extract_all_metadata(content)
                self.save_content_metadata(metadata, prompt_path)

                # Save full metadata as JSON
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)

                if metadata["has_prompt"]:
                    items_with_prompts += 1

                self.stats["prompts_saved"] += 1
            else:
                self.stats["errors"] += 1

            # Rate limiting
            time.sleep(0.5)

        # Summary for this model
        print(f"   ✓ Images: {len([f for f in images_dir.iterdir() if f.is_file()])}")
        print(f"   ✓ Videos: {len([f for f in videos_dir.iterdir() if f.is_file()])}")
        print(f"   ✓ Items with prompts: {items_with_prompts}")

        self.stats["models_processed"] += 1

    def download_from_csv(self, csv_path: str, max_models: Optional[int] = None,
                          max_items_per_model: Optional[int] = None,
                          download_videos: bool = True,
                          download_images: bool = True,
                          only_with_prompts: bool = False):
        """Download all content from models in CSV"""
        print("\n" + "="*70)
        print("🌐 UNIVERSAL CIVITAI CONTENT DOWNLOADER")
        print("="*70)

        # Load data
        df = pd.read_csv(csv_path)

        if max_models:
            df = df.head(max_models)

        print(f"\nModels to process: {len(df)}")
        if max_items_per_model:
            print(f"Max items per model: {max_items_per_model}")
        print(f"Download videos: {'Yes' if download_videos else 'No'}")
        print(f"Download images: {'Yes' if download_images else 'No'}")
        print(f"Only with prompts: {'Yes' if only_with_prompts else 'No'}")
        print(f"Output directory: {self.output_dir}")
        print("\n" + "="*70)

        # Download from each model
        for idx, row in df.iterrows():
            try:
                self.download_model_all_content(
                    row.to_dict(),
                    max_items_per_model,
                    download_videos,
                    download_images
                )

                # Status update every 10 models
                if (idx + 1) % 10 == 0:
                    self.print_stats()

            except Exception as e:
                print(f"Error processing model {row.get('model_name')}: {e}")
                self.stats["errors"] += 1

        # Final stats
        print("\n" + "="*70)
        print("✅ DOWNLOAD COMPLETE!")
        print("="*70)
        self.print_stats()

    def print_stats(self):
        """Print download statistics"""
        print(f"\n📊 Statistics:")
        print(f"  Models processed: {self.stats['models_processed']}")
        print(f"  Images downloaded: {self.stats['images_downloaded']}")
        print(f"  Videos downloaded: {self.stats['videos_downloaded']}")
        print(f"  Articles found: {self.stats['articles_found']}")
        print(f"  Prompts saved: {self.stats['prompts_saved']}")
        print(f"  Total size: {self.stats['total_size_mb']:.1f} MB")
        print(f"  Errors: {self.stats['errors']}")


if __name__ == "__main__":
    # Example usage
    downloader = UniversalCivitaiDownloader(output_dir="./all_content")

    # Download EVERYTHING from first 10 models
    downloader.download_from_csv(
        csv_path="./outputs/civitai_fixed_20251124_161134.csv",
        max_models=10,
        max_items_per_model=20,  # More items per model
        download_videos=True,     # Include videos
        download_images=True      # Include images
    )
