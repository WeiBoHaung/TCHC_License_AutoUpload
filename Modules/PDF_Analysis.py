import os,sys
import time
import pdfplumber
from datetime import datetime


wd = os.getcwd()

class PDF_Analysis:
    def __init__(self,fileName):
        self.path=wd+'\License\\'+fileName
        self.pdf=pdfplumber.open(self.path)
        self.table_setting={
            # "vertical_strategy": "explicit", 
            # "horizontal_strategy": "explicit",
            # "explicit_vertical_lines": [],
            # "explicit_horizontal_lines": [],
            "snap_tolerance": 6,
            # "join_tolerance": 3,
            # "edge_min_length": 3,
            # "min_words_vertical": 3,
            # "min_words_horizontal": 1,
            # "keep_blank_chars": False,
            # "text_tolerance": 3,
            # "text_x_tolerance": None,
            # "text_y_tolerance": None,
            # "intersection_tolerance": 3,
            # "intersection_x_tolerance": None,
            # "intersection_y_tolerance": None,
        }

    def exportData(self):
        for page in self.pdf.pages:
            print(page.extract_text())
            print(page.chars[0],page.extract_table(self.table_setting))

if __name__ == '__main__':
    pdfFile=PDF_Analysis("通過認證時數證書11007011600.pdf")
    pdfFile.exportData()


        