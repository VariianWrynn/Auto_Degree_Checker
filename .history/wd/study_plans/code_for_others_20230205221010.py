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

    dir_name = './wd/processed_studyplan_csvs/tabel_like_csvs_unfinished'
    
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
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import os

# # Open a PDF file.
# fp = open(r"D:/CS_Uni/auto degree checker/wd/study_plans/studyplans_pdf/mix/b-compsci-AIlMajors-S1-2023_FINAL.pdf", 'rb')

def parse_obj(lt_objs, page):

    # loop over the object list
    for obj in lt_objs:
        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            if ( 680 < (obj.bbox[1]) < 690):
                # print ("%6d" % (obj.bbox[0]))
                # print ("%6d" % (obj.bbox[1]))
                for filename in os.listdir(dir_name):
                    if filename.endswith('.csv'):
                        print(filename[-5])
                        print(f"page number:  {page}")
                        #if filename[-5] is NOT a digit, then we will process it, else we skip it
                        if (filename[-5].isdigit()):
                            if (int(filename[-5]) == int(page)):
                                print("\n########## Major found: MAJOR NAME: ##############")
                                print("%s" % (obj.get_text()))
                                filename = os.path.join(dir_name, filename)
                                new_filename = obj.get_text().replace('\n', '') + ".csv"
                                new_filename = os.path.join(dir_name, new_filename)
                                new_filename.replace(" ","")
                                print(new_filename)
                                # if not os.path.exists(dir_name):
                                os.rename(filename, new_filename)
                                print(filename)
                # print('\n')

        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs, page)


if __name__ == '__main__':

    for pdf_file in os.listdir(pdf_dir):

        pdf_file_path = pdf_dir + "/" + pdf_file
        print("\n############### Processing: ##################")
        print(pdf_file)
        degree_name = pdf_file.replace(".pdf", "")
        dir_name = dir_mker(degree_name)
        produce_full_csv(pdf_file_path, dir_name)
        fliter_csv(dir_name)
        print(pdf_file_path)

        fp = open(pdf_file_path, 'rb')

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Create a PDF device object.
        device = PDFDevice(rsrcmgr)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)


        # loop over all pages in the document
        for page in PDFPage.create_pages(document):
            print('NEXT PAGE')

            # read the page into a layout object
            interpreter.process_page(page)
            layout = device.get_result()

            # extract text from this object
            parse_obj(layout._objs, layout.pageid)

