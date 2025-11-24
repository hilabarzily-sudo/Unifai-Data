"""
Run full download of images and prompts
"""

from image_downloader import CivitaiImageDownloader
import sys

def main():
    # Configuration
    csv_path = "./outputs/civitai_fixed_20251124_161134.csv"
    output_dir = "./downloads"
    max_models = 100  # Start with 100 most popular models
    max_images_per_model = 10

    print("\n" + "="*70)
    print("🚀 STARTING FULL DOWNLOAD")
    print("="*70)
    print(f"Models: {max_models}")
    print(f"Max images per model: {max_images_per_model}")
    print(f"Output: {output_dir}/")
    print("="*70)
    print("\nPress Ctrl+C to stop at any time...")
    print("="*70 + "\n")

    try:
        downloader = CivitaiImageDownloader(output_dir=output_dir)
        downloader.download_from_csv(
            csv_path=csv_path,
            max_models=max_models,
            max_images_per_model=max_images_per_model
        )

    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        print("\nPartial results saved to:", output_dir)
        downloader.print_stats()
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
