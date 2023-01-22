import tabula
import os
import pandas as pd

pdf_path = r"D:/CS_Uni/auto degree checker/wd/study_plans/studyplans_pdf/mix/b-compsci-AIlMajors-S1-2023_FINAL.pdf"
dir_name = './wd/processed_studyplan_csvs'

if not os.path.exists(dir_name):
        os.mkdir(dir_name)

dir_name = './wd/processed_studyplan_csvs/tabel_like_csvs_unfinished'

if not os.path.exists(dir_name):
        os.mkdir(dir_name)

# Create a dir called "cache" which store all produced csvs
def produce_full_csv(pdf_path):

    dfs = tabula.read_pdf(pdf_path, pages = 'all')

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
 
    for page_num in range(len(dfs)):
        outname = f"table_{page_num}.csv"
        fullname = os.path.join(dir_name, outname)
        dfs[page_num].to_csv(fullname)

def fliter_csv(dir_name):
    for filename in os.listdir(dir_name):
        # read CSV file
        filename = os.path.join(dir_name, filename)
        results = pd.read_csv(filename)
        # count no. rows         count no. cloumns 
        if len(results) < 13 or len(results.axes[1]) < 5:
            print(f"file to be removed: {filename}")
            os.remove(filename)


if __name__ == '__main__':
    produce_full_csv(pdf_path)
    fliter_csv(dir_name)
