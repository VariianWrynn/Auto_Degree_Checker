from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
import io
from pdfminer.layout import LTTextBox
import re

def extract_text_at_coords(pdf_path, coords):
    xmin, ymin, xmax, ymax = coords
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
                    if xmin < element.bbox[0] < xmax and ymin < element.bbox[1] < ymax:
                        text = re.sub(r'\s+', ' ', element.get_text().strip())
                        print(text)

# test the function
coords = (100, 100, 200, 200)
extract_text_at_coords(r'test\1.pdf', coords)
