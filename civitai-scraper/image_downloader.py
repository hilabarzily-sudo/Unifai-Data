"""
Civitai Image & Prompt Downloader
Downloads all images with their prompts, organized by model
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


class CivitaiImageDownloader:
    """Downloads images and prompts from Civitai models"""

    def __init__(self, output_dir: str = "./downloads"):
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
            "prompts_saved": 0,
            "errors": 0
        }

    def sanitize_filename(self, name: str) -> str:
        """Clean filename for filesystem"""
        # Remove invalid characters
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        # Remove emojis and special unicode
        name = re.sub(r'[^\x00-\x7F]+', '_', name)
        # Limit length
        name = name[:100]
        return name.strip()

    def get_model_images(self, model_id: int) -> List[Dict]:
        """Fetch all images for a specific model"""
        try:
            response = self.session.get(
                f"{self.base_url}/models/{model_id}",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            all_images = []

            # Get images from all model versions
            for version in data.get("modelVersions", []):
                images = version.get("images", [])
                for img in images:
                    img["version_name"] = version.get("name", "unknown")
                    img["version_id"] = version.get("id")
                    all_images.append(img)

            return all_images

        except Exception as e:
            print(f"Error fetching model {model_id}: {e}")
            return []

    def download_image(self, url: str, save_path: Path) -> bool:
        """Download single image"""
        try:
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True

        except Exception as e:
            print(f"Error downloading image: {e}")
            return False

    def extract_prompt(self, image_data: Dict) -> Dict:
        """Extract prompt and metadata from image"""
        metadata = {
            "prompt": "",
            "negative_prompt": "",
            "steps": None,
            "sampler": None,
            "cfg_scale": None,
            "seed": None,
            "model": None,
            "width": image_data.get("width"),
            "height": image_data.get("height"),
            "nsfw": image_data.get("nsfw"),
            "image_url": image_data.get("url"),
        }

        # Extract from meta field
        meta = image_data.get("meta", {})
        if meta:
            metadata["prompt"] = meta.get("prompt", "")
            metadata["negative_prompt"] = meta.get("negativePrompt", "")
            metadata["steps"] = meta.get("steps")
            metadata["sampler"] = meta.get("sampler")
            metadata["cfg_scale"] = meta.get("cfgScale")
            metadata["seed"] = meta.get("seed")
            metadata["model"] = meta.get("Model")

        return metadata

    def save_prompt(self, prompt_data: Dict, save_path: Path):
        """Save prompt to text file"""
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                if prompt_data["prompt"]:
                    f.write("=== PROMPT ===\n")
                    f.write(prompt_data["prompt"] + "\n\n")

                if prompt_data["negative_prompt"]:
                    f.write("=== NEGATIVE PROMPT ===\n")
                    f.write(prompt_data["negative_prompt"] + "\n\n")

                f.write("=== SETTINGS ===\n")
                f.write(f"Steps: {prompt_data['steps']}\n")
                f.write(f"Sampler: {prompt_data['sampler']}\n")
                f.write(f"CFG Scale: {prompt_data['cfg_scale']}\n")
                f.write(f"Seed: {prompt_data['seed']}\n")
                f.write(f"Model: {prompt_data['model']}\n")
                f.write(f"Size: {prompt_data['width']}x{prompt_data['height']}\n")

        except Exception as e:
            print(f"Error saving prompt: {e}")

    def download_model_images(self, model_data: Dict, max_images: Optional[int] = None):
        """Download all images and prompts for a single model"""
        model_id = model_data.get("model_id")
        model_name = model_data.get("model_name", f"model_{model_id}")

        # Create model directory
        safe_name = self.sanitize_filename(model_name)
        model_dir = self.output_dir / safe_name
        images_dir = model_dir / "images"
        prompts_dir = model_dir / "prompts"

        images_dir.mkdir(parents=True, exist_ok=True)
        prompts_dir.mkdir(parents=True, exist_ok=True)

        # Get images
        images = self.get_model_images(model_id)

        if not images:
            print(f"No images found for {model_name}")
            return

        # Limit if specified
        if max_images:
            images = images[:max_images]

        print(f"\n📥 Downloading {len(images)} images from: {model_name}")

        # Save model metadata
        model_metadata = {
            "model_id": model_id,
            "model_name": model_name,
            "model_url": model_data.get("model_url"),
            "type": model_data.get("type"),
            "downloads": model_data.get("downloads"),
            "creator": model_data.get("creator_username"),
            "base_model": model_data.get("base_model"),
            "total_images": len(images),
        }

        with open(model_dir / "model_info.json", 'w', encoding='utf-8') as f:
            json.dump(model_metadata, f, indent=2, ensure_ascii=False)

        # Download each image
        for idx, img_data in enumerate(tqdm(images, desc=f"  {model_name[:40]}")):
            image_id = img_data.get("id", idx)
            image_url = img_data.get("url")

            if not image_url:
                continue

            # Determine file extension
            ext = "png"
            if "jpeg" in image_url.lower() or "jpg" in image_url.lower():
                ext = "jpg"
            elif "webp" in image_url.lower():
                ext = "webp"

            # File paths
            image_filename = f"image_{idx+1:03d}_{image_id}.{ext}"
            prompt_filename = f"image_{idx+1:03d}_{image_id}_prompt.txt"
            metadata_filename = f"image_{idx+1:03d}_{image_id}_metadata.json"

            image_path = images_dir / image_filename
            prompt_path = prompts_dir / prompt_filename
            metadata_path = prompts_dir / metadata_filename

            # Skip if already downloaded
            if image_path.exists():
                continue

            # Download image
            if self.download_image(image_url, image_path):
                self.stats["images_downloaded"] += 1

                # Extract and save prompt
                prompt_data = self.extract_prompt(img_data)
                self.save_prompt(prompt_data, prompt_path)

                # Save full metadata as JSON
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(prompt_data, f, indent=2, ensure_ascii=False)

                self.stats["prompts_saved"] += 1
            else:
                self.stats["errors"] += 1

            # Rate limiting
            time.sleep(0.3)

        self.stats["models_processed"] += 1

    def download_from_csv(self, csv_path: str, max_models: Optional[int] = None,
                          max_images_per_model: Optional[int] = None):
        """Download images from all models in CSV"""
        print("\n" + "="*70)
        print("🖼️  CIVITAI IMAGE & PROMPT DOWNLOADER")
        print("="*70)

        # Load data
        df = pd.read_csv(csv_path)

        if max_models:
            df = df.head(max_models)

        print(f"\nModels to process: {len(df)}")
        if max_images_per_model:
            print(f"Max images per model: {max_images_per_model}")
        print(f"Output directory: {self.output_dir}")
        print("\n" + "="*70)

        # Download from each model
        for idx, row in df.iterrows():
            try:
                self.download_model_images(row.to_dict(), max_images_per_model)

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
        print(f"  Prompts saved: {self.stats['prompts_saved']}")
        print(f"  Errors: {self.stats['errors']}")


if __name__ == "__main__":
    # Example usage
    downloader = CivitaiImageDownloader(output_dir="./downloads")

    # Download from CSV (limit to first 10 models, 5 images each for testing)
    downloader.download_from_csv(
        csv_path="./outputs/civitai_fixed_20251124_161134.csv",
        max_models=10,
        max_images_per_model=5
    )
