import os
import re
import logging

def get_files(path: str) -> list:
    first_directory = True
    files_to_scan = []

    if os.path.isdir(path):
        for dirpath, _, files in os.walk(path):
            for file_name in files:

                if first_directory:
                    files_to_scan.append(dirpath + '\\' + file_name)
                    logging.debug(f'Got file path: {dirpath + '\\' + file_name}')
                    continue
                
                files_to_scan.append(dirpath + file_name)
                logging.debug(f'Got file path: {dirpath + file_name}')

            first_directory = False
    
    return files_to_scan
    

def validate_files(path: str,
                   media: str,
                   sensory: str) -> list:
    """
    Finds the necessary and valid files for scanning
    """
    
    media_filter = []
    sensory_filter = []

    image = {'png', 'jpeg', 'jpg', 'bmp'}
    video = {'mp4', 'mkv', 'mov'}
    audio = {'wav', 'ogg', 'mp3'}

    
    # Scans through the file extension of a list of files
    def scan_file_extension(files, filter, output):
        logging.debug(f'Iterating {len(files)} file(s), allowing {filter}')
        filter = set.union(*filter)

        for file in files:
            match = re.search(r"\.([^.]+)$", file)
            if match.group(1) in filter:
                output.append(file)
    

    # Filters for media files
    if media == 'all':
        scan_file_extension(path, [image, video, audio], media_filter)
    elif media == 'image':
        scan_file_extension(path, [image], media_filter)
    elif media == 'video':
        scan_file_extension(path, [video], media_filter)
    elif media == 'audio':
        scan_file_extension(path, [audio], media_filter)

    
    # Filters for sensory
    if sensory == 'all':
        scan_file_extension(media_filter, [image, video, audio], sensory_filter)
    elif sensory == 'vision':
        scan_file_extension(media_filter, [image, video], sensory_filter)
    elif sensory == 'auditory':
        scan_file_extension(media_filter, [video, audio], sensory_filter)


    # Replace with validated files
    logging.debug('Validated Files according to the settings')
    path = sensory_filter
    return path