"""
Download EVERYTHING - Ready for D:\unifai_data_catch
Downloads all images, videos, prompts, articles, posts
"""

from universal_downloader import UniversalCivitaiDownloader
import os
import shutil
from pathlib import Path

def main():
    # Configuration
    csv_path = "./outputs/civitai_fixed_20251124_161134.csv"

    # Output will be prepared for Windows path: D:\unifai_data_catch
    output_dir = "./unifai_data_catch"  # Local copy, ready to transfer

    # Download settings
    max_models = 100  # Start with 100 models (change to 2000 for all)
    max_items_per_model = 30  # More items = more videos/images

    print("\n" + "="*70)
    print("🌐 DOWNLOADING EVERYTHING FOR UNIFAI")
    print("="*70)
    print(f"Will download:")
    print(f"  ✓ Images (with prompts)")
    print(f"  ✓ Videos (with prompts)")
    print(f"  ✓ Articles & Descriptions")
    print(f"  ✓ All metadata")
    print(f"\nModels: {max_models}")
    print(f"Max items per model: {max_items_per_model}")
    print(f"\nLocal output: {output_dir}/")
    print(f"Transfer to: D:\\unifai_data_catch\\")
    print("="*70 + "\n")

    try:
        # Create downloader
        downloader = UniversalCivitaiDownloader(output_dir=output_dir)

        # Download EVERYTHING
        downloader.download_from_csv(
            csv_path=csv_path,
            max_models=max_models,
            max_items_per_model=max_items_per_model,
            download_videos=True,    # Include videos
            download_images=True,    # Include images
            only_with_prompts=False  # Get everything, even without prompts
        )

        print("\n" + "="*70)
        print("✅ DOWNLOAD COMPLETE!")
        print("="*70)

        # Create transfer instructions
        create_transfer_guide(output_dir)

    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        print(f"\nPartial results saved to: {output_dir}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def create_transfer_guide(output_dir: str):
    """Create instructions for transferring to Windows"""
    guide_path = Path(output_dir) / "TRANSFER_TO_WINDOWS.txt"

    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("HOW TO TRANSFER TO D:\\unifai_data_catch\n")
        f.write("="*70 + "\n\n")

        f.write("METHOD 1: Direct Copy (if on same machine)\n")
        f.write("-" * 70 + "\n")
        f.write("1. Copy the entire 'unifai_data_catch' folder\n")
        f.write("2. Paste to D:\\ drive\n")
        f.write("3. Final path should be: D:\\unifai_data_catch\\\n\n")

        f.write("METHOD 2: SCP/SFTP Transfer\n")
        f.write("-" * 70 + "\n")
        f.write("# From Linux to Windows:\n")
        f.write("scp -r ./unifai_data_catch your-windows-user@your-windows-ip:D:\\\n\n")

        f.write("METHOD 3: Archive and Transfer\n")
        f.write("-" * 70 + "\n")
        f.write("# Create archive:\n")
        f.write("tar -czf unifai_data_catch.tar.gz unifai_data_catch/\n\n")
        f.write("# Or zip:\n")
        f.write("zip -r unifai_data_catch.zip unifai_data_catch/\n\n")
        f.write("# Then transfer the archive file\n\n")

        f.write("METHOD 4: Mount Windows Drive\n")
        f.write("-" * 70 + "\n")
        f.write("# If D: drive is accessible:\n")
        f.write("mkdir -p /mnt/d\n")
        f.write("mount -t drvfs D: /mnt/d\n")
        f.write("cp -r unifai_data_catch /mnt/d/\n\n")

        f.write("="*70 + "\n")
        f.write("FOLDER STRUCTURE\n")
        f.write("="*70 + "\n\n")
        f.write("D:\\unifai_data_catch\\\n")
        f.write("├── [Model Name 1]/\n")
        f.write("│   ├── images/           # All images\n")
        f.write("│   ├── videos/           # All videos\n")
        f.write("│   ├── prompts/          # All prompts & metadata\n")
        f.write("│   ├── articles/         # Descriptions & articles\n")
        f.write("│   └── model_info.json\n")
        f.write("├── [Model Name 2]/\n")
        f.write("└── ...\n\n")

        f.write("="*70 + "\n")
        f.write("QUICK STATS\n")
        f.write("="*70 + "\n")
        f.write(f"Total models: Check the folder count\n")
        f.write(f"Total size: Run 'du -sh {output_dir}'\n")

    print(f"\n📝 Transfer guide created: {guide_path}")
    print(f"\n📦 Your data is ready in: {output_dir}/")
    print(f"   Copy this folder to: D:\\unifai_data_catch\\")


if __name__ == "__main__":
    main()
