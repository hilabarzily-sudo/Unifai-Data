#!/usr/bin/env python3
"""
Civitai Categorized Downloader
Downloads all content organized by model type (LORA, Checkpoint, etc.)
Saves directly to D:\\unifai_data_catch
"""

import json
import time
from pathlib import Path
from typing import Dict, List
from tqdm import tqdm
import pandas as pd
from universal_downloader import UniversalCivitaiDownloader

class CategorizedDownloader:
    """Downloads Civitai content organized by categories"""

    def __init__(self, csv_path: str, output_root: str = "./unifai_data_catch"):
        """
        Initialize categorized downloader

        Args:
            csv_path: Path to CSV with model data
            output_root: Root directory for downloads (will organize by categories)
        """
        self.csv_path = csv_path
        self.output_root = Path(output_root)
        self.downloader = UniversalCivitaiDownloader(output_dir=str(self.output_root))

        # Category mapping
        self.categories = {
            'LORA': 'LORA',
            'Checkpoint': 'Checkpoint',
            'Workflows': 'Workflows',
            'LoCon': 'LoCon',
            'TextualInversion': 'TextualInversion',
            'DoRA': 'DoRA',
            'Wildcards': 'Wildcards',
            'VAE': 'VAE',
            'Other': 'Other'
        }

    def load_models_by_category(self) -> Dict[str, List[Dict]]:
        """Load models from CSV and organize by category"""
        print("\n" + "="*70)
        print("📂 LOADING MODELS FROM CSV")
        print("="*70 + "\n")

        models_by_category = {cat: [] for cat in self.categories.values()}

        # Use pandas to read CSV (handles types better)
        df = pd.read_csv(self.csv_path)

        for _, row in df.iterrows():
            model_dict = row.to_dict()
            model_type = model_dict.get('type', 'Other')
            category = self.categories.get(model_type, 'Other')
            models_by_category[category].append(model_dict)

        # Print statistics
        print("📊 Models by Category:")
        print("-" * 70)
        total = 0
        for category, models in sorted(models_by_category.items(),
                                       key=lambda x: len(x[1]),
                                       reverse=True):
            count = len(models)
            total += count
            print(f"  {category:20s}: {count:5d} models")
        print("-" * 70)
        print(f"  {'TOTAL':20s}: {total:5d} models\n")

        return models_by_category

    def create_category_structure(self):
        """Create directory structure for all categories"""
        print("📁 Creating category directories...")
        for category in self.categories.values():
            category_dir = self.output_root / category
            category_dir.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {category}/")
        print()

    def download_category(self, category: str, models: List[Dict],
                         max_items_per_model: int = 30):
        """
        Download all content for a specific category

        Args:
            category: Category name (LORA, Checkpoint, etc.)
            models: List of model dictionaries
            max_items_per_model: Max images/videos per model
        """
        if not models:
            print(f"⏭️  Skipping {category} - no models")
            return

        print("\n" + "="*70)
        print(f"📥 DOWNLOADING: {category}")
        print("="*70)
        print(f"Models to process: {len(models)}")
        print(f"Max items per model: {max_items_per_model}")
        print(f"Output: {self.output_root / category}")
        print("="*70 + "\n")

        # Set output directory for this category
        category_dir = self.output_root / category

        # Create a fresh downloader for this category (so stats start at 0)
        category_downloader = UniversalCivitaiDownloader(output_dir=str(category_dir))

        stats = {
            'models_processed': 0,
            'images_downloaded': 0,
            'videos_downloaded': 0,
            'prompts_saved': 0,
            'errors': 0
        }

        for model in tqdm(models, desc=f"📦 {category}", unit="model"):
            try:
                model_id = model.get('model_id')
                if not model_id:
                    continue

                # Download all content for this model
                category_downloader.download_model_all_content(
                    model_data=model,
                    max_items=max_items_per_model,
                    download_videos=True,
                    download_images=True
                )

                # Small delay to avoid rate limiting
                time.sleep(0.3)

            except Exception as e:
                stats['errors'] += 1
                print(f"\n❌ Error with model {model.get('model_name', 'unknown')}: {e}")
                continue

        # Get final stats from downloader
        stats['models_processed'] = category_downloader.stats.get('models_processed', 0)
        stats['images_downloaded'] = category_downloader.stats.get('images_downloaded', 0)
        stats['videos_downloaded'] = category_downloader.stats.get('videos_downloaded', 0)
        stats['prompts_saved'] = category_downloader.stats.get('prompts_saved', 0)
        stats['errors'] += category_downloader.stats.get('errors', 0)

        # Print category statistics
        print("\n" + "-"*70)
        print(f"📊 {category} Statistics:")
        print(f"  Models processed: {stats['models_processed']}")
        print(f"  Images downloaded: {stats['images_downloaded']}")
        print(f"  Videos downloaded: {stats['videos_downloaded']}")
        print(f"  Prompts saved: {stats['prompts_saved']}")
        print(f"  Errors: {stats['errors']}")
        print("-"*70 + "\n")

        # Save category statistics
        stats_file = category_dir / f"{category.lower()}_stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)

        return stats

    def download_all(self, max_items_per_model: int = 30,
                    categories_to_download: List[str] = None):
        """
        Download all categories

        Args:
            max_items_per_model: Max images/videos per model
            categories_to_download: List of specific categories to download
                                   (None = all)
        """
        print("\n" + "="*70)
        print("🚀 CIVITAI CATEGORIZED DOWNLOADER")
        print("="*70)
        print(f"CSV File: {self.csv_path}")
        print(f"Output Root: {self.output_root}")
        print(f"Max items per model: {max_items_per_model}")
        print("="*70 + "\n")

        # Load models
        models_by_category = self.load_models_by_category()

        # Create directory structure
        self.create_category_structure()

        # Filter categories if specified
        if categories_to_download:
            models_by_category = {
                cat: models for cat, models in models_by_category.items()
                if cat in categories_to_download
            }

        # Download each category
        total_stats = {
            'categories_processed': 0,
            'total_models': 0,
            'total_images': 0,
            'total_videos': 0,
            'total_prompts': 0,
            'total_errors': 0
        }

        for category, models in sorted(models_by_category.items(),
                                       key=lambda x: len(x[1]),
                                       reverse=True):
            stats = self.download_category(category, models, max_items_per_model)

            if stats:
                total_stats['categories_processed'] += 1
                total_stats['total_models'] += stats['models_processed']
                total_stats['total_images'] += stats['images_downloaded']
                total_stats['total_videos'] += stats['videos_downloaded']
                total_stats['total_prompts'] += stats['prompts_saved']
                total_stats['total_errors'] += stats['errors']

        # Print final statistics
        print("\n" + "="*70)
        print("🎉 DOWNLOAD COMPLETE!")
        print("="*70)
        print(f"Categories processed: {total_stats['categories_processed']}")
        print(f"Total models: {total_stats['total_models']}")
        print(f"Total images: {total_stats['total_images']}")
        print(f"Total videos: {total_stats['total_videos']}")
        print(f"Total prompts: {total_stats['total_prompts']}")
        print(f"Total errors: {total_stats['total_errors']}")
        print("="*70)
        print(f"\n📍 All content saved to: {self.output_root}")
        print("\n💡 To transfer to Windows D:\\ drive:")
        print(f"   1. Archive: tar -czf unifai_data.tar.gz {self.output_root}")
        print("   2. Transfer to Windows and extract to D:\\unifai_data_catch\n")

        # Save total statistics
        stats_file = self.output_root / "total_stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(total_stats, f, indent=2)


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Download Civitai content organized by categories'
    )
    parser.add_argument(
        '--csv',
        default='outputs/civitai_fixed_20251124_161134.csv',
        help='Path to CSV file with model data'
    )
    parser.add_argument(
        '--output',
        default='./unifai_data_catch',
        help='Output root directory (default: ./unifai_data_catch)'
    )
    parser.add_argument(
        '--max-items',
        type=int,
        default=30,
        help='Max images/videos per model (default: 30)'
    )
    parser.add_argument(
        '--categories',
        nargs='+',
        help='Specific categories to download (default: all)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: download only first 5 models per category'
    )

    args = parser.parse_args()

    # Create downloader
    downloader = CategorizedDownloader(
        csv_path=args.csv,
        output_root=args.output
    )

    # Test mode: limit models
    if args.test:
        print("\n⚠️  TEST MODE: Will download only 5 models per category\n")
        models_by_category = downloader.load_models_by_category()
        for category in models_by_category:
            models_by_category[category] = models_by_category[category][:5]

        downloader.create_category_structure()

        for category, models in models_by_category.items():
            if models:
                downloader.download_category(category, models, args.max_items)
    else:
        # Full download
        downloader.download_all(
            max_items_per_model=args.max_items,
            categories_to_download=args.categories
        )


if __name__ == '__main__':
    main()
