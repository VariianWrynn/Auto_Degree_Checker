import re
import csv
import PyPDF2
import os

dir_name = r'wd\transcript_operation'

if not os.path.exists(dir_name):
        os.mkdir(dir_name)

# Open the P DF file in read-binary mode
with open(r'wd\user_transcript\transcript.pdf', 'rb') as file:
  # Create a PDF reader object
  reader = PyPDF2.PdfReader(file)

  # Open a CSV file for writing
  with open(rf'{dir_name}\cache.csv', 'w', newline='') as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)

    # Iterate over every page in the PDF
    for page in reader.pages:
      # Extract the text from the page
      text = page.extract_text()

      # Split the text into lines
      lines = text.split('\n')

      # Flag to track if we have found the keyword
      found_keyword = False

      # Iterate over every line in the text
      for line in lines:
        # Check if the line contains the keyword
        if 'Enrolment Summary' in line:
          # Set the flag to true
          found_keyword = True
        elif found_keyword:
          # If the keyword has been found and this line is below it, split the line into fields by 3 or more spaces
          fields = re.split(r' {8,}', line)
          # Write the fields to the CSV file
          writer.writerow(fields)


# Open the CSV file for reading
with open(rf'{dir_name}\cache.csv', 'r', newline='') as input_file:
  # Create a CSV reader object
  reader = csv.reader(input_file)

  # Open a new CSV file for writing
  with open(rf'{dir_name}\courses_done_ID.csv', 'w', newline='') as output_file:
    # Create a CSV writer object
    writer = csv.writer(output_file)

    # Iterate over every row in the CSV file
    for row in reader:
      # Use a regular expression to delete the leading set of 4 numbers
      row = [re.sub(r'^\d{4}', '', field) for field in row]
      row = [re.sub(r' {2,}', ' ', field) for field in row]
      # Use a regular expression to remove the leading space from each field
      row = [re.sub(r'^\s*', '', field) for field in row]
      # Use a regular expression to delete the first string and a space
      row = [re.sub(r'^\w+\s', '', field) for field in row]
      # Use a regular expression to delete the space and keep everything until a set of 4 numbers
      row = [re.sub(r'(\d{4}).*', r'\1', field) for field in row]
      del row[-1]
      # Iterate over every row in the CSV file
      # Skip the row if it is an empty list
      if not row:
        continue
      # Skip the row if the first field is an empty string
      if row[0] == '':
        continue
      # Write the modified row to the new CSV file
      writer.writerow(row)

# Delete the CSV file
os.remove(rf'{dir_name}\cache.csv')
# os.rename("output1.csv", "courses_done_ID.csv")
