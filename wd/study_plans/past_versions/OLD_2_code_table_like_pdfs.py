import camelot
import os
import pandas as pd

pdf_path = r"D:/CS_Uni/auto degree checker/wd/study_plans/studyplans_pdf/mix/b-compsci-AIlMajors-S1-2023_FINAL.pdf"

def pdf_path_handler(pdf_path):
    dir_name = './wd/processed_studyplan_csvs'

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    dir_name = './wd/processed_studyplan_csvs/tabel_like_csvs_unfinished'
    
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


if __name__ == '__main__':
    dir_name = pdf_path_handler(pdf_path)
    produce_full_csv(pdf_path, dir_name)
    fliter_csv(dir_name)