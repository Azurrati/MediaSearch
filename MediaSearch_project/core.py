import sys
import re
import importlib.util
import hashlib
from rich import print

class Core_Components:
    @staticmethod
    def validate_configuration(path, media, sensory, confidence):
        from MediaSearch_project import validator
        
        check_settings = validator.validate_settings(media, sensory, confidence)
        validate_path = validator.validate_path(path)
    
        try:
            validator.accept_configuration(check_settings, validate_path)
        except Exception as e:
            print('Configuration was not accepted.')
            print(e)
            print('Exiting.')
            sys.exit(1)


    def start_files(self, path, media, sensory):
        from MediaSearch_project import files

        get_files = files.get_files(path)
        validated_files = files.validate_files(get_files, media, sensory)

        self.files_total = len(validated_files)

        return validated_files


    def scan(self, files, ocr, sr, sr_model, time, confidence, search_words, verbose):
        from MediaSearch_project import search
        from MediaSearch_project.scanners import(
            image as image_engine,
            video as video_engine,
            audio as audio_engine
        )

        image_type = {'png', 'jpeg', 'jpg', 'bmp'}
        video_type = {'mp4', 'mkv', 'mov'}
        audio_type = {'wav', 'ogg', 'mp3'}

        file_data = {}
        files_scanned = 0

        try:
            for file in files:
                file_type = re.search(r"\.([^.]+)$", file).group(1)

                with open(file, "rb") as f:
                    hash_object = hashlib.file_digest(f, "sha256")
                    hash_file = hash_object.hexdigest()
                f.close()

                files_scanned += 1
                print(f'[[green]+[/green]] Scanning file [yellow]{file}[/yellow] [{files_scanned}/{self.files_total}]')

                if file_type in image_type:
                    data = image_engine.scan(file, ocr)
                elif file_type in video_type:
                    data = video_engine.scan(file, ocr, time)
                elif file_type in audio_type:
                    data = audio_engine.scan(file, sr_model)
                else:
                    raise AssertionError(f'An unrecognized file type appeared. The file was \"{file}\"')

                file_data[file] = {}

                if file_type in image_type:
                    file_data[file]["ocr_engine"] = ocr
                    file_data[file]["sha256"] = hash_file
                    file_data[file]["ocr_text"] = data
                    search_result = search.search(search_words, data, confidence)

                elif file_type in video_type:
                    file_data[file]["ocr_engine"] = ocr
                    file_data[file]["sha256"] = hash_file
                    file_data[file]["Frames"] = {}
                    for time, text in data:
                        file_data[file]["Frames"][f"Frame {time}"] = text
                        search_result = search.search(search_words, text, confidence)

                elif file_type in audio_type:
                    file_data[file]["sha256"] = hash_file
                    for segment, text in data:
                        file_data[file]["Segments"][segment] = text
                        search_result = search.search(search_words, text, confidence)

                        if search.decode(search_result):
                            file_data[file]["Found Keywords"]["Segment"] = segment

                text_result = search.decode(search_result, verbose)

                if text_result:
                    print(f'[[blue]-[/blue]] [blue]Info:[/blue] {text_result}')
                elif text_result == []:
                    print(f'[[blue]-[/blue]] [blue]Info:[/blue] [red]No Text Detected.[/red]')

        except KeyboardInterrupt:
            print('[[red]![/red]] [red]Keyboard Interrupt Detected! Saving...[/red]')
        except Exception as e:
            print(f'[[red]![/red]] [red]An error occurred: {e}[/red]')
        finally:
            return file_data


    @staticmethod
    def check_libraries():
        libraries = ['rapidfuzz', 'paddleocr', 'pytesseract', 'faster_whisper', 'easyocr', 'rich']

        for library in libraries:
            if importlib.util.find_spec(library) is None:
                print(f'[[red]![/red]] [red]Library \"{library}\" is not installed. Exiting.[/red]')
                sys.exit(1)


    @staticmethod
    def output(text_data):
        from MediaSearch_project import output

        output.json_file.create_file(text_data)
        
    

def main(path, media, sensory, search, ocr, time, confidence, sr, sr_model, verbosity):
    print('[[green]+[/green]] [green]MediaSearch - A tool to search for text in Images, Videos, and Audio[/green]')
    
    core_components = Core_Components()

    core_components.check_libraries()
    core_components.validate_configuration(path, media, sensory, confidence)

    validated_files = core_components.start_files(path, media, sensory)
    text_data = core_components.scan(validated_files, ocr, sr, sr_model, time, confidence, search, verbosity)

    core_components.output(text_data)