def validate_settings(media = None, sensory = None, confidence = None) -> tuple:
    """
    Codes:
    0 - Non-existent Setting
    1 - Invalid Setting
    2 - Valid Setting

    Error Type:
    0 - No Error
    1 - Audio sensory cannot be put on image file
    2 - Vision sensory cannot be put on auditory
    3 - Beyond Minimum/Maximum confidence
    """

    if media == 'image' and sensory == 'auditory':
        return (1,1)
    if media == 'audio' and sensory == 'vision':
        return (1,2)
    if (confidence > 100) or (confidence < 0):
        return (1,3)
    
    return (2,0)


def validate_path(path: str) -> bool:
    import os 

    if os.path.exists(path):
        return True
    else:
        return False


def accept_configuration(settings, path):
    Error_code = {
        0: 'Non-existent Setting',
        1: 'Invalid Setting',
        2: 'Valid Setting'
    }

    Error_type = {
        0: 'No Error',
        1: 'Audio sensory cannot be put on image',
        2: 'Vision sensory cannot be put on audio',
        3: 'Beyond Minimum/Maximum confidence'
    }

    if settings[0] < 2:
        raise TypeError(f'Error Code: {Error_code[settings[0]]} | Error Type: {Error_type[settings[1]]}')

    if not path:
        raise FileNotFoundError(f'File path \"{path}\" does not exist.')