# MediaDateSorter

**MediaDateSorter** is a Python script designed to efficiently sort and organize media files based on either their embedded creation dates or recognizable filename patterns. Ideal for consolidating diverse media collections from various sources.

## Features

- **Date Extraction**: Utilizes embedded metadata or filenames with a `YYYYMMDD` pattern.
- **Automatic Dependency Handling**: Installs missing libraries as needed.
- **Logging**: Generates `media_sorter.log` for action tracking and troubleshooting.
- **Supports formats**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.mp4`, `.mov`, `.avi`, `.mkv`, `.heic`, `.3gp`, `.dng`, `.m4v`.
- **Fallback**: Files without clear dates are safely placed in an "unsorted" directory.

## Dependencies

- Pillow (for reading image metadata)
- tqdm (for displaying a progress bar)

## Prerequisites

- A Python installation.
- Compatible with Linux, Windows, and Mac.
- Necessary permissions to install dependencies. On Windows, ensure you're running as an administrator. For Linux/Mac, `sudo` might be required.

## Usage

1. Either download or clone the repo to obtain `mediadatesorter.py`.
2. Change to your media directory.
3. You have two options to run the script:
   - Using command-line arguments to specify source and destination directories:
     ```
     python mediadatesorter.py -s SOURCE_DIRECTORY -d DESTINATION_DIRECTORY
     ```
   - Running the script without arguments, and then follow the instructions on the screen to input the source and destination directories:
     ```
     python mediadatesorter.py
     ```

Please replace `SOURCE_DIRECTORY` and `DESTINATION_DIRECTORY` with your actual paths when using command-line arguments.

## Important Notes

- **File Movement**: This script moves (not copies) files. Ensure you've backed up your data before proceeding.
- **Performance**: For extensive collections, consider running during off-peak times or ensuring your system has ample resources.
- **Customization**: The script can be easily modified to support additional file types or filename prefixes.
  
## Known Filename Prefixes

Files starting with the following prefixes won't have their dates extracted:

- FB_IMG_
- Snapchat-
- IMG-WA
- VID-WA
- Instagram-
- Twitter-
- Screenshot_
- WIN_
- MVIMG_
- PANO_
- BURST_
- SM_
- Screen Shot
- Skype-
- Zoom-
- PhotoCollage_
- Collage_
- Clip_
- Export_
- Download_
- Edited_

These prefixes are defined within the script, and you may modify them to suit your specific use case.

## Logging

A `media_sorter.log` file will be created, capturing actions and potential issues. Refer to this for troubleshooting or to track the sorting process.

## Contributions

If this is hosted publicly (e.g., on GitHub), consider contributing to enhance the script, report issues, or request additional features.

## License

MIT License.

---