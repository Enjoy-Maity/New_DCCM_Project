import os
import pandas as pd

class Excel_Reader:
    def __init__(self, file_path: str, dict: bool = False, df: bool = True):
        if os.path.exists(str(file_path)):
            self.file_path = str(file_path)
        
        else:
            raise FileNotFoundError("File Not Found!")