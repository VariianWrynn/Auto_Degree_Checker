from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBox
from pdfminer.layout import LTTextLine
import numpy as np
import os
import re
import sys

csv_dir = r"D:\CS_Uni\auto degree checker\Auto_Degree_Checker\wd_test\processed_studyplan_csvs\table_like_csvs\b-eng-eee-allmajors-bmcs-compscimajor-S1-2023_FINAL"


def extract_coords_from_pdf(pdf_path, search_string):
    rows = 1
    cols = 5
    arr = np.empty((rows, cols))
    # open the pdf file
    with open(pdf_path, 'rb') as file:
        # create pdf resource manager
        rsrcmgr = PDFResourceManager()
        # create a pdf page aggregator
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)
            layout = device.get_result()
            # iterate over all the text boxes in the layout
            for element in layout:
              if isinstance(element, LTTextBox):
                if element.get_text().strip() == search_string:

                  # print(f"{search_string} found in the PDF.")
                  coords = element.bbox
                  # print(coords)
                  xmin, ymin, xmax, ymax = coords

                  xmin += 232
                  ymin += 20
                  xmax += 270
                  ymax += 26 

                  data = np.array([int(xmin), int(ymin), int(xmax), int(ymax), layout.pageid])

                  if (np.size(arr) == 1):
                    arr = data
                  else:
                    arr = np.append(arr, [data], axis = 0)
    return arr


def extract_text_at_coords(pdf_path, coords):
  # for i in range(len(coords)):
    
    # print(xmin, ymin, xmax, ymax, pageid)
    # open the pdf file
    with open(pdf_path, 'rb') as file:
      # Create a PDF parser object associated with the file object.
        parser_1 = PDFParser(file)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document_1 = PDFDocument(parser_1)
        # Check if the document allows text extraction. If not, abort.
        if not document_1.is_extractable:
            raise PDFTextExtractionNotAllowed
        # create pdf resource manager
        rsrcmgr_1 = PDFResourceManager()

        device_1 = PDFDevice(rsrcmgr_1)

        # create a pdf page aggregator
        laparams_1 = LAParams()

        device_1 = PDFPageAggregator(rsrcmgr_1, laparams=laparams_1)
        interpreter_1 = PDFPageInterpreter(rsrcmgr_1, device_1)
        # pages = PDFPage.get_pages(file)
        coords_index = 0

        for page in PDFPage.create_pages(document_1):
            if coords_index >= len(coords):
              print("The end of coords array has been reached, program Completed")
              sys.exit()

            xmin, ymin, xmax, ymax, pageid = coords[coords_index]

            interpreter_1.process_page(page)
            layout_1 = device_1.get_result()

            # loop-breaker will be set to true when a correct ccsv file is detected
            loop_breaker = False
            for csv_file in os.listdir(csv_dir):
              if loop_breaker: break

              if csv_file.endswith('.csv'):
                if (csv_file[-5].isdigit()):
                  if (csv_file[-6].isdigit()):

                    if int(csv_file[-6] + csv_file[-5]) == int(pageid):
                    # iterate over all the text boxes in the layout
                      for obj in layout_1._objs:
                          if isinstance(obj, LTTextBox) or isinstance(obj, LTTextLine):
                            # print(re.sub(r'\s+', ' ', obj.get_text().strip()))
                            xmin_condition = (int(xmin) - 200 <= int(obj.bbox[0]) <= int(xmin) + 10)
                            ymin_condition = (int(ymin) - 5 <= int(obj.bbox[1]) <= int(ymin) + 5)
                            xmax_condition = (int(xmax) - 10 <= int(obj.bbox[2]) <= int(xmax) + 10)
                            ymax_condition = (int(ymax) - 5 <= int(obj.bbox[3]) <= int(ymax) + 5)
                            if xmin_condition and ymin_condition and xmax_condition and ymax_condition:
                              coords_index += 1
                              text = re.sub(r'\s+', ' ', obj.get_text().strip())
                              print(text)
                              loop_breaker = True
                              break
                  else:
                    if (int(csv_file[-5]) == int(pageid)):
                        for obj in layout_1._objs:
                            if isinstance(obj, LTTextBox) or isinstance(obj, LTTextLine):
                              xmin_condition = (int(xmin) - 200 <= int(obj.bbox[0]) <= int(xmin) + 10)
                              ymin_condition = (int(ymin) - 5 <= int(obj.bbox[1]) <= int(ymin) + 5)
                              xmax_condition = (int(xmax) - 10 <= int(obj.bbox[2]) <= int(xmax) + 10)
                              ymax_condition = (int(ymax) - 5 <= int(obj.bbox[3]) <= int(ymax) + 5)
                              if xmin_condition and ymin_condition and xmax_condition and ymax_condition:
                                coords_index += 1
                                text = re.sub(r'\s+', ' ', obj.get_text().strip())
                                print(text)
                                loop_breaker = True
                                break
                      



result = extract_coords_from_pdf(rf'test\1.pdf', "Year 1")
result = np.delete(result, 0, axis=0)
print(result.astype(int)) 

extract_text_at_coords(rf'test\1.pdf', result.astype(int))
