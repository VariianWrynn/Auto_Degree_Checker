import re
import csv
import PyPDF2

input_pdf = r"D:\CS_Uni\auto degree checker\wd\study_plans\studyplans_pdf\mix\b-maths-compsci-S1-2023_FINAL (1).pdf"
cache_csv = 'cache.csv'
output_csv = 'output.csv'

def pdf_to_csv():
    try:
        # Open the PDF file in read-binary mode
        with open(input_pdf, 'rb') as file:
            # Create a PDF reader object
            reader = PyPDF2.PdfReader(file)

            # Open a CSV file for writing
            with open(cache_csv, 'w', newline='') as csv_file:
                # Create a CSV writer object
                writer = csv.writer(csv_file)

                # Iterate over every page in the PDF
                for page in reader.pages:
                    # Extract the text from the page
                    text = page.extract_text()
                    # Split the text into lines
                    lines = text.split('\n')
                    writer.writerow(lines)
                    
    except FileNotFoundError:
        print(f'Error: Input PDF file "{input_pdf}" not found')
    except PyPDF2.PdfReadError:
        print(f'Error: Input PDF file "{input_pdf}" is invalid or corrupted')

def delete_columns():
        # Open the CSV file in read mode
    with open(cache_csv, 'r') as input_file:
    # Create a CSV reader object
        reader = csv.reader(input_file)
    # Read the rows of the CSV file into a list of rows
        rows = [row for row in reader]
    # Delete the first 9 columns from each row
        for row in rows:
            del row[:9]

    # Open the CSV file in write mode, with the same filename as the input file
    with open(cache_csv, 'w', newline='') as output_file:
        # Create a CSV writer object
        writer = csv.writer(output_file)
        # Write the modified rows to the CSV file
        writer.writerows(rows)
    # remove the unnecessary variable cache_csv_2




def extract_cells():
    try:
        with open(cache_csv) as csv_file:
            # create a CSV reader object
            reader = csv.reader(csv_file)
            # Read the rows of the CSV file into a list of rows
            rows = [row for row in reader]
            # iterate through the rows of the CSV file
            for row in rows:
                for cell in row:
                # find the index of the word in the row
                        pattern = re.compile(r'\bMajor\b|\bMinor\b')
                        # Iterate over the rows and cells of the CSV file
                            # Use the regular expression to search for the word "major" in the cell
                        match = pattern.search(cell)
                        if match:
                            index = row.index(cell)
                            # extract the cells to the right of the word
                            cells = row[index:]
                            yield cells
                        else:
                            # word not found in the row, skip it
                            continue
    except FileNotFoundError:
        print(f'Error: Cache CSV file "{cache_csv}" not found')


def delete_space():
    # Compile a regular expression pattern to match cells containing multiple spaces
    pattern = re.compile(r'^\s+$')

    # Open the input file in read mode
    with open('output.csv', 'r') as input_csv:
        # Create a CSV reader object
        reader = csv.reader(input_csv)
        # Read the rows of the CSV file into a list of rows
        rows = [row for row in reader]

    # Store the initial length of the rows list
    rows_length = len(rows)

    # Initialize the index
    i = 0

    # Use a while loop instead of a for loop
    while i < rows_length:
        # Iterate over the cells of the row
        for j in range(len(rows[i])):
            match = pattern.search(rows[i][j])
            # Check if the cell is empty
            if match:
                print(f'#### Empty cell detected at i: {i} and j: {j} ####')
                # Get the rest of the cells in the current row
                rest_of_row = rows[i][j+1:]
                # Remove the rest of the cells from the current row
                del rows[i][j+1:]
                new_row = rest_of_row
                # Insert the rest of the cells into the next row
                rows.insert(i+1, new_row)
                # Increase the length of the rows list
                rows_length += 1
                break
        # Move to the next row
        i += 1
        # Open the output file in write mode
        
    with open('output.csv', 'w', newline='') as output_csv:
            # Create a CSV writer object
        writer = csv.writer(output_csv)
            # Write the modified rows to the output file
        writer.writerows(rows)
                

def delete_empty_rows():
    # Compile a regular expression pattern to match rows containing only whitespaces
    pattern = re.compile(r'^\s*$')
    # Open the input file in read mode
    with open(output_csv, 'r') as input_file:
        # Create a CSV reader object
        reader = csv.reader(input_file)
        # Read the rows of the CSV file into a list
        rows = [row for row in reader]
    # Iterate over the rows of the CSV file
    i = 0
    while i < len(rows):
        # check if the row is empty or only contains whitespaces
        if pattern.match(''.join(rows[i])):
            # Delete the row
            del rows[i]
        else:
            i += 1
    # Open the file in write mode
    with open(output_csv, 'w', newline='') as output_file:
        # Create a CSV writer object
        writer = csv.writer(output_file)
        # Write the modified rows to the CSV file
        writer.writerows(rows)



############USE CASE#############
pdf_to_csv()
delete_columns()

# open the output file
try:
    with open(output_csv, 'w', newline='') as output_file:
            # create a CSV writer object
            writer = csv.writer(output_file)
            # iterate over the extracted cells
            for cells in extract_cells():
                # write the cells to the output file
                writer.writerow(cells)
except OSError:
    print(f'Error: Output CSV file "{output_csv}" could not be created or written to')

delete_space()

delete_empty_rows()
