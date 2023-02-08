import os
# folder_name = "wd"

import re
import shutil

file_path = 'wd\study_plans\studyplans_pdf'

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