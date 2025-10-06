"""
CSV file handling utilities
"""

import csv
from pathlib import Path
from typing import Dict


class CSVHandler:
    def __init__(self, filepath: str, headers: list):
        self.filepath = filepath
        self.headers = headers
    
    def append(self, data: Dict[str, str]):
        """
        Append data to CSV file
        
        Creates file with headers if it doesn't exist
        """
        file_exists = Path(self.filepath).exists()
        
        with open(self.filepath, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(data)