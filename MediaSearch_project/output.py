import json
import os
import rich
from datetime import datetime

# class terminal:
#     def intro():
#         print('[+] MediaSearch - A tool to search for text in Images, Videos, and Audio')

#     def output_scans(total, current):
#         pass

class json_file:
    @staticmethod
    def create_file(text_data):
        # Create result file
        if not os.path.exists('.results'):
            os.mkdir('.results')

        # Generate report under .results
        now = datetime.now()
        string_date = now.strftime("%Y-%m-%d %H:%M:%S")

        string_date_file = now.strftime("%Y-%m-%d %H-%M-%S")

        data = {
            "time": f"{string_date}",
            "files": text_data
        }

        # Write search results
        with open(f".results\\{string_date_file}.json", "w") as file:
            json.dump(data, file, indent=4)
        