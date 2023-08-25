import os
import shutil
import re
import logging
import sys
import ctypes
import argparse
from datetime import datetime

DEPENDENCIES = {
    "Pillow": "PIL",  # Package name: Import name
    "tqdm": "tqdm"
}

def initialize_logging():
    logging.basicConfig(filename='media_sorter.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to check if the script is running with administrative privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Check and install necessary dependencies
def install_dependencies(dependencies):
    for package_name in dependencies.keys():
        try:
            import importlib
            importlib.import_module(dependencies[package_name])
        except ImportError:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"{package_name} has been installed.")

if not is_admin():
    print("This script requires administrative privileges to install dependencies.")
    sys.exit(1)

install_dependencies(DEPENDENCIES)

from PIL import Image
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description="Sort and organize media files")
    parser.add_argument("-s", "--source", help="Path to the source directory", required=False)
    parser.add_argument("-d", "--destination", help="Path to the destination directory", required=False)
    return parser.parse_args()

def get_creation_date(file_path):
    try:
        # Try to get the creation date from the image metadata
        image = Image.open(file_path)
        info = image._getexif()
        
        if info and 36867 in info:
            date_str = info[36867]
            return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        pass

    return None

def extract_date_from_filename(filename):
    # List of known prefixes that shouldn't be interpreted as dates
    non_date_prefixes = [
        "FB_IMG_", "Snapchat-", "IMG-WA", "VID-WA", "Instagram-", "Twitter-",
        "Screenshot_", "WIN_", "MVIMG_", "PANO_", "BURST_", 
        "SM_", "Screen Shot", "Skype-", "Zoom-", "PhotoCollage_", "Collage_", 
        "Clip_", "Export_", "Download_", "Edited_"
    ]
    
    # Check if filename starts with any of the known prefixes
    if any(filename.startswith(prefix) for prefix in non_date_prefixes):
        return None

    # Check if the filename matches the YYYYMMDD pattern
    match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
    if match:
        year, month, day = match.groups()
        try:
            date_obj = datetime(int(year), int(month), int(day))
            # Validate the year is within a reasonable range
            current_year = datetime.now().year
            if 1900 <= date_obj.year <= current_year:
                return date_obj
        except ValueError:
            return None
    return None

def move_file_based_on_date(file_path, dest_dir, counters):
    date = get_creation_date(file_path)
    
    if date:
        month_name = date.strftime('%B')
        year_month_dir = os.path.join(dest_dir, "sorted", str(date.year), f"{date.month:02} - {month_name}")
    else:
        date_from_filename = extract_date_from_filename(os.path.basename(file_path))
        if date_from_filename:
            month_name = date_from_filename.strftime('%B')
            year_month_dir = os.path.join(dest_dir, "sorted", str(date_from_filename.year), f"{date_from_filename.month:02} - {month_name}", "filename-dated")
        else:
            year_month_dir = os.path.join(dest_dir, "unsorted")
            counters["unsorted"] += 1
    
    if not os.path.exists(year_month_dir):
        os.makedirs(year_month_dir)
    
    shutil.move(file_path, os.path.join(year_month_dir, os.path.basename(file_path)))
    counters["moved"] += 1

def sort_media(source_dir, dest_dir):
    counters = {"moved": 0, "unsorted": 0}
    
    # Get a list of all files first for tqdm
    all_files = [os.path.join(root, file) for root, dirs, files in os.walk(source_dir) for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.mp4', '.mov', '.avi', '.mkv', '.heic', '.3gp', '.dng', '.m4v'))]
    
    for file_path in tqdm(all_files, desc="Sorting media", unit="file"):
        move_file_based_on_date(file_path, dest_dir, counters)
    
    return counters

def check_free_space(dest_dir, required_space):
    total, used, free = shutil.disk_usage(dest_dir)
    return free > required_space

if __name__ == "__main__":
    initialize_logging()
    
    args = parse_arguments()
    source_directory = args.source if args.source else input("Enter the source directory path: ")
    destination_directory = args.destination if args.destination else "."  # Assuming current directory as the destination

    # Validate the source directory
    if not os.path.isdir(source_directory):
        print(f"Error: {source_directory} is not a valid directory.")
        sys.exit(1)
    
    # Calculate required space - this is a rough estimate, for example based on the size of source files
    total_size = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(source_directory) for file in files)
    
    # Check for free space in the destination directory
    if not check_free_space(destination_directory, total_size):
        print(f"Error: Not enough free space in the destination directory.")
        sys.exit(1)

    results = sort_media(source_directory, destination_directory)
    print(f"Sorting and moving completed! {results['moved']} files moved. {results['unsorted']} files couldn't be sorted.")
    logging.info(f"{results['moved']} files moved. {results['unsorted']} files couldn't be sorted.")