#!/usr/bin/env python3
"""
Download and setup FooDB data for enriching your food database.

This script helps you download FooDB data and prepares it for use
with the FooDBImporter.

FooDB is ~87 MB (JSON) to ~953 MB (CSV) - the script will guide you.
"""

import os
import urllib.request
import tarfile
import zipfile
from pathlib import Path


FOODB_URLS = {
    # Note: These URLs may change. Visit https://foodb.ca/downloads for current links
    "json": "https://foodb.ca/system/downloads/foodb_2020_4_7_json.zip",
    "csv": "https://foodb.ca/system/downloads/foodb_2020_4_7_csv.tar.gz",
    "mysql": "https://foodb.ca/system/downloads/foodb_2020_4_7_sql.tar.gz",
}


def download_file(url: str, output_path: Path, chunk_size: int = 8192) -> None:
    """Download a file with progress indicator."""
    print(f"Downloading from: {url}")
    print(f"Saving to: {output_path}")
    print()
    
    def report_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(100, downloaded * 100 / total_size)
        mb_downloaded = downloaded / (1024 * 1024)
        mb_total = total_size / (1024 * 1024)
        print(f"\rProgress: {percent:.1f}% ({mb_downloaded:.1f} MB / {mb_total:.1f} MB)", end="")
    
    urllib.request.urlretrieve(url, output_path, reporthook=report_progress)
    print()  # New line after progress
    print(f"Download complete: {output_path}")


def extract_archive(archive_path: Path, output_dir: Path) -> None:
    """Extract tar.gz or zip file."""
    print(f"Extracting {archive_path.name}...")
    
    if archive_path.suffix == ".zip":
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
    elif archive_path.suffix == ".gz" or str(archive_path).endswith(".tar.gz"):
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(output_dir)
    
    print(f"Extracted to: {output_dir}")


def setup_foodb_data():
    """Main setup function."""
    print("=" * 70)
    print("FooDB Data Download & Setup")
    print("=" * 70)
    print()
    
    # Create data directory
    data_dir = Path("data/foodb")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Data will be saved to: {data_dir.absolute()}")
    print()
    
    # Check if already downloaded
    existing_files = list(data_dir.glob("*"))
    if existing_files:
        print("Existing files found:")
        for f in existing_files[:10]:  # Show first 10
            print(f"  - {f.name}")
        if len(existing_files) > 10:
            print(f"  ... and {len(existing_files) - 10} more")
        print()
        
        response = input("FooDB data seems to already exist. Re-download? (y/n): ").lower()
        if response != 'y':
            print("Using existing data.")
            return data_dir
    
    # Choose format
    print("Available formats:")
    print("  1. JSON (~87 MB) - RECOMMENDED: Fast loading, smaller size")
    print("  2. CSV (~953 MB) - Full relational data")
    print("  3. MySQL Dump (~173 MB) - For database import")
    print()
    
    choice = input("Select format (1-3) [default: 1]: ").strip() or "1"
    
    format_map = {"1": "json", "2": "csv", "3": "mysql"}
    selected_format = format_map.get(choice, "json")
    
    url = FOODB_URLS[selected_format]
    filename = url.split("/")[-1]
    download_path = data_dir / filename
    
    # Download
    try:
        print()
        print(f"Downloading FooDB {selected_format.upper()} format...")
        print("This may take a few minutes depending on your connection.")
        print()
        
        download_file(url, download_path)
        
        # Extract
        print()
        extract_archive(download_path, data_dir)
        
        print()
        print("=" * 70)
        print("Setup Complete!")
        print("=" * 70)
        print()
        print(f"FooDB data is ready at: {data_dir}")
        print()
        print("You can now use it with:")
        print("  from blutwerte.foods.importers import FooDBImporter")
        print("  importer = FooDBImporter()")
        
        if selected_format == "json":
            print(f'  importer.load_from_json("{data_dir}/foodb_2020_4_7_json/FooDB.json")')
        else:
            print(f'  importer.load_from_csv("{data_dir}")')
        
        return data_dir
        
    except Exception as e:
        print(f"Error downloading: {e}")
        print()
        print("You can manually download from:")
        print("  https://foodb.ca/downloads")
        print()
        return None


def verify_setup(data_dir: Path) -> bool:
    """Verify that FooDB data is properly set up."""
    print()
    print("Verifying FooDB setup...")
    
    # Check for JSON file
    json_files = list(data_dir.glob("**/FooDB.json"))
    if json_files:
        print(f"✓ Found FooDB JSON: {json_files[0]}")
        return True
    
    # Check for CSV files
    csv_files = list(data_dir.glob("**/*.csv"))
    if csv_files:
        print(f"✓ Found {len(csv_files)} CSV files")
        return True
    
    print("✗ FooDB data not found")
    return False


if __name__ == "__main__":
    data_dir = setup_foodb_data()
    
    if data_dir:
        verify_setup(data_dir)
