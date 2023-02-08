import logging

logging.basicConfig(filename='wd\study_plans\code_for_others.log', format='#(name)s - %(levelname)s')

############### PDF_TABLE EXTRACTION TO A CSV FILE ##################
import camelot
import os
import pandas as pd

#this is where original pdf files should be
pdf_dir = "wd/study_plans/studyplans_pdf/others"

def dir_mker(degree_name):
    # this is where you want to store all finished csv file
    dir_name = './wd/processed_studyplan_csvs'

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    dir_name = './wd/processed_studyplan_csvs/tabel_like_csvs'
    
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    
    dir_name = dir_name + "/" + degree_name

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    return dir_name


def produce_full_csv(pdf_path, dir_name):
    #read the pdf file
    tables = camelot.read_pdf(pdf_path, pages = 'all')
    #print the number of tables extracted
    # print("Number of tables extracted: ", len(tables))

    for i in range(tables.n):
        table = tables[i]
        page = table.parsing_report['page']
        table.to_csv(f"{dir_name}\Table{i+1}_page{page}.csv")


def fliter_csv(dir_name):
    for filename in os.listdir(dir_name):
        # read CSV file
        filename = os.path.join(dir_name, filename)
        results = pd.read_csv(filename)

        # the first cell (row 1, col 1) in a study plan table should contain precisily "Year 1"
        if results.axes[1][0] != 'Year 1':
            os.remove(filename)


################ FILE RENAMING ################


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
import numpy as np
import os
import re


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


                    if data[-1] == arr[-1][-1]: continue
                    arr = np.append(arr, [data], axis = 0)
                    break
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
            print("The end of coords array has been reached, entire file has been processed")
            return 

          xmin, ymin, xmax, ymax, pageid = coords[coords_index]

          interpreter_1.process_page(page)
          layout_1 = device_1.get_result()

          # loop-breaker will be set to true when a correct ccsv file is detected
          loop_breaker = False
          for csv_file in os.listdir(dir_name):
            if loop_breaker: break
            if csv_file.endswith('.csv'):
              if (csv_file[-5].isdigit()):
                if (csv_file[-6].isdigit()):

                  if int(csv_file[-6] + csv_file[-5]) == int(pageid) and layout_1.pageid == int(pageid):
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
                                  major_name = re.sub(r'\s+', ' ', obj.get_text().strip())

                                  print(major_name)

                                  csv_file = os.path.join(dir_name, csv_file)
                                  new_filename = major_name + ".csv"
                                  new_filename = os.path.join(dir_name, new_filename)
                                  new_filename = new_filename.replace(' .csv','.csv')
                                  os.rename(csv_file, new_filename)

                                  loop_breaker = True
                                  break
                else:
                  if (int(csv_file[-5]) == int(pageid)) and layout_1.pageid == int(pageid):
                      for obj in layout_1._objs:
                          if isinstance(obj, LTTextBox) or isinstance(obj, LTTextLine):
                              xmin_condition = (int(xmin) - 200 <= int(obj.bbox[0]) <= int(xmin) + 10)
                              ymin_condition = (int(ymin) - 5 <= int(obj.bbox[1]) <= int(ymin) + 5)
                              xmax_condition = (int(xmax) - 10 <= int(obj.bbox[2]) <= int(xmax) + 10)
                              ymax_condition = (int(ymax) - 5 <= int(obj.bbox[3]) <= int(ymax) + 5)
                              if xmin_condition and ymin_condition and xmax_condition and ymax_condition:
                                  coords_index += 1
                                  major_name = re.sub(r'\s+', ' ', obj.get_text().strip())

                                  print(major_name)

                                  csv_file = os.path.join(dir_name, csv_file)
                                  new_filename = major_name + ".csv"
                                  new_filename = os.path.join(dir_name, new_filename)
                                  new_filename = new_filename.replace(' .csv','.csv')
                                  os.rename(csv_file, new_filename)

                                  loop_breaker = True

                                  break

      if coords_index == 0: print("No major was specificed on the study plan")





if __name__ == '__main__':

    for pdf_file in os.listdir(pdf_dir):

        pdf_file_path = pdf_dir + "/" + pdf_file
        print("\n############### Processing: ##################")
        print(pdf_file)
        degree_name = pdf_file.replace(".pdf", "")
        dir_name = dir_mker(degree_name)
        produce_full_csv(pdf_file_path, dir_name)
        fliter_csv(dir_name)

        coords = np.empty((1,5))
        

        coords = extract_coords_from_pdf(pdf_file_path, "Year 1")
        coords = np.delete(coords, 0, axis=0)

        extract_text_at_coords(pdf_file_path, coords)



