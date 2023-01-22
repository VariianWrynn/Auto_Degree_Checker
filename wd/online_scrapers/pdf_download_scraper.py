from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import csv
import os
import shutil
import logging
import re

file_path = 'wd\study_plans\studyplans_pdf'

# Set up logging
logging.basicConfig(filename='wd\online_scrapers\errors.log', level=logging.ERROR)

print("Current working directory: {0}".format(os.getcwd()))

ID=0

with open('wd\online_scrapers\set_study_plans_links.csv', 'r', encoding='UTF-8') as csv_file:
  csv_reader = csv.reader(csv_file)
  for row in csv_reader:
    print(ID)
    ID = ID + 1
    link = row[-1]
    print("\n#######################LINK##################\n")
    print(link)
    print("\n#######################LINK##################\n")

    ChromeOptions = Options()
    ChromeOptions.add_argument("start-maximized")

    prefs = {"download.default_directory": os.path.abspath(file_path)}

    # json_str = json.dumps(list(prefs))

    ChromeOptions.add_experimental_option("prefs", prefs)
    # options.add_experimental_option("prefs", {'download.default_directory': r'wd\study_plans\studyplans_pdf\ALL_studyplans'})
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=ChromeOptions)
    driver.get(link)

    # Wait for 5 seconds to load the webpage completely
    time.sleep(10)

    try:
        # Find the button using text
        driver.find_element('xpath','//*[@id="app"]/div[5]/span/div/main/div/div/div[1]/header/div/div/div/button').click()
    except Exception as e:
        # An exception will be raised if the button cannot be found or clicked
        # In this case, we will log the error and continue to the next iteration
        logging.error(f'Error processing link {link}: {e}')
        continue
    except: 
        logging.error(e)

    time.sleep(10)

    # Close the driver
    driver.close()


########Putting fownloaded pdfs into the right folder##########

# Check if the folders exists in the directory, if not create them
if not os.path.exists(os.path.join(file_path, "b_math_and_cs")):
    os.mkdir(os.path.join(file_path, "b_math_and_cs"))
if not os.path.exists(os.path.join(file_path, "others")):
    os.mkdir(os.path.join(file_path, "others"))

    # Loop through all the files in the directoryv n;wq
for file in os.listdir(file_path):
    if file.endswith(".pdf"):
        file = re.sub(r"\s+.pdf", ".pdf", file)

# Loop through all the files in the directoryv n;wq
for file in os.listdir(file_path):

    if file.endswith(".pdf"):
        # file = re.sub(r"\s+.pdf", ".pdf", file)
        # Check if the file name contains "b_math"
        if "b-maths" in file:
            # Move the file to the "b_math_and_cs" folder
            shutil.move(os.path.join(file_path, file), os.path.join(file_path, "b_math_and_cs"))
        else:
            # Move the file to the "others" folder
            shutil.move(os.path.join(file_path, file), os.path.join(file_path, "others"))

