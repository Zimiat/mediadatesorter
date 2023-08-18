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

    # If we can't get the creation date from the metadata, use the file's modification date
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp)

def move_file_based_on_date(file_path, dest_dir):
    date = get_creation_date(file_path)
    year_month_dir = os.path.join(dest_dir, "sorted", str(date.year), str(date.month).zfill(2))
    
    if not os.path.exists(year_month_dir):
        os.makedirs(year_month_dir)
    
    shutil.move(file_path, os.path.join(year_month_dir, os.path.basename(file_path)))

def sort_media(source_dir, dest_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.mp4', '.mov', '.avi', '.mkv')):
                move_file_based_on_date(os.path.join(root, file), dest_dir)

if __name__ == "__main__":
    source_directory = input("Enter the source directory path: ")
    destination_directory = input("Enter the destination directory path: ")

    sort_media(source_directory, destination_directory)
    print("Sorting and moving completed!")