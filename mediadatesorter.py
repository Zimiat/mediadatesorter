import re
import os
import shutil
from PIL import Image
from datetime import datetime

# Check and install necessary dependencies
try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

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
    # Check if the filename matches the YYYYMMDD pattern
    match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
    if match:
        year, month, day = match.groups()
        try:
            return datetime(int(year), int(month), int(day))
        except ValueError:
            return None
    return None

def move_file_based_on_date(file_path, dest_dir):
    date = get_creation_date(file_path)
    
    if date:
        month_name = date.strftime('%B')
        year_month_dir = os.path.join(dest_dir, "sorted", str(date.year), f"{date.month:02} - {month_name}")
    else:
        date_from_filename = extract_date_from_filename(os.path.basename(file_path))
        if date_from_filename:
            year_month_dir = os.path.join(dest_dir, str(date_from_filename.year), "nodata")
        else:
            year_month_dir = os.path.join(dest_dir, "unsorted")
    
    if not os.path.exists(year_month_dir):
        os.makedirs(year_month_dir)
    
    shutil.move(file_path, os.path.join(year_month_dir, os.path.basename(file_path)))

def sort_media(source_dir, dest_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.mp4', '.mov', '.avi', '.mkv', '.heic', '.3gp', '.dng', '.m4v')):
                move_file_based_on_date(os.path.join(root, file), dest_dir)

if __name__ == "__main__":
    source_directory = input("Enter the source directory path: ")
    destination_directory = "."  # Assuming current directory as the destination

    sort_media(source_directory, destination_directory)
    print("Sorting and moving completed!")