# MediaDateSorter

After downloading all my Google Photos and OneDrive content, I was confronted with the challenge of organizing and indexing them for long-term storage. The sheer volume and disorganization made the task daunting. That's why I created MediaDateSorter - a Python script designed to streamline the process of sorting media files based on their creation dates. Whether the date is embedded in the file's metadata, hinted in the filename, or even absent, this tool will help you declutter and categorize your media efficiently.

## Features

- **Metadata Sorting**: Organizes media files based on embedded metadata dates.
- **Filename Date Extraction**: For files without metadata dates, the script checks for dates in the filename pattern `YYYYMMDD`.
- **Fallback to Unsorted**: Media files without recognizable dates are moved to an "unsorted" directory.
- **Automatic Dependency Installation**: If required libraries are missing, the script will attempt to install them.
- **Supports Multiple Formats**: Compatible with `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.mp4`, `.mov`, `.avi`, `.mkv`, `.heic`, `.3gp`, `.dng`, and `.m4v`.

## How to Use

### Prerequisites

- Python 3.x

### Steps

1. Download the `MediaDateSorter.py` script from this repository.
2. Place the script in the directory containing the media files you want to sort.
3. Navigate to the directory in your terminal or command prompt and run the script:
```
python MediaDateSorter.py
```
4. When prompted, enter the source directory path containing the media files you want to sort.
5. The script will automatically sort the media files and move them to the appropriate directories (`./sorted`, `./year/nodata`, or `./unsorted`).

## Contributing

Contributions are welcome! Feel free to fork this repository, make your improvements, and then submit a pull request.

## License

This project is licensed under the MIT License.
