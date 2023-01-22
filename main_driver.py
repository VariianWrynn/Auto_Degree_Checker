import os
import sys
folder_name = "wd"

if __name__ == '__main__':

    # Get the current working directory
    cwd = os.getcwd()
    print(cwd)

    # Check if the folder exists in the current working directory
    if not os.path.exists(os.path.join(cwd, folder_name)):
        print(f"{folder_name} does not exist in the current working directory, current working directory is: {cwd}")
        print(f"Please change your working directory to where you have cloned the git repo")
        print(f"cloned git repo should contain a folder called: {folder_name}") 
        sys.exit()

    # ###### Download study plans (in pdf) ############
    exec(open(f"{cwd}\wd\online_scrapers\pdf_download_scraper.py").read())

    ###### extract informations on pdf files to csv files ############
    exec(open(f"{cwd}\wd\study_plans\code_for_b_math_compsci.py").read())
    exec(open(f"{cwd}\wd\study_plans\code_for_others.py").read())

    ###### extract information on user's transcript to csv files #########
    exec(open(rf"{cwd}\wd\transcript_operation\transcript_extract.py").read())