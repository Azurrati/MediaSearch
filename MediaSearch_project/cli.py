import argparse

def main():
    # Creates arguments and parses them
    parser = argparse.ArgumentParser(description='Find Words in Media Files like Images, Video, and Audio.')

    parser.add_argument(
        'path',
        type=str,
        help='Selects a folder or file path.'
    )

    parser.add_argument(
        '-v',
        action="store_true",
        help='Enables Verbosity'
    )
    
    parser.add_argument(
        '--media',
        type=str,
        choices=['image', 'video', 'audio', 'all'],
        default='all',
        help='Select text on which media file.'
    )
    
    parser.add_argument(
        '--sensory',
        type=str,
        choices=['vision', 'auditory', 'all'],
        default='all',
        help='Selects the type of sensory.'
    )
    
    parser.add_argument(
        '--search',
        type=str,
        nargs='*',
        help='Searches for keywords.'
    )
    
    parser.add_argument(
        '--confidence',
        type=int,
        default=90,
        help='How confident the OCR engine is, at the keyword'
    )
    
    parser.add_argument(
        '--ocr',
        type=str,
        choices=['Tesseract', 'EasyOCR', 'PaddleOCR'],
        default='PaddleOCR',
        help='Sets an OCR engine. \"PaddleOCR\" is the default'
    )

    parser.add_argument(
        '--sr',
        type=str,
        choices=['Faster-Whisper'],
        default='Faster-Whisper',
        help='Sets an Speech Recognition engine. \"Faster-Whisper\" is the default'
    )

    parser.add_argument(
        '--sr_model',
        type=str,
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        default='base',
        help='Sets an model for SR engine, \"base\" is the default'
    )

    parser.add_argument(
        '--s',
        type=float,
        default=1,
        help='OCR once every amount of seconds. Acronym for \"Scan per second\". An Alternative command for fps is \"--fps\".'
    )

    # parser.add_argument(
    #     '--fps',
    #     type=float,
    #     help='OCR once every amount of frames. Acronym for \"Frames per second\". An Alternative command for seconds is \"--sps\".'
    # )

    args = parser.parse_args()

    from MediaSearch_project import core
    core.main(args.path,
              args.media,
              args.sensory,
              args.search,
              args.ocr,
              args.s,        # FPS and seconds need to point to here
              args.confidence,
              args.sr,
              args.sr_model,
              args.v
              )