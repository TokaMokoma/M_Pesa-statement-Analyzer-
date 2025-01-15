import streamlit as st
import pdfplumber
import csv

def uploadPDF(PDF, csv_path):
    # Open the PDF file
    with pdfplumber.open(PDF) as pdf, open(csv_path, 'w', newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)  # Use the opened file object here

        #  # Create/open the CSV file for writing
        #     with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        #         csv_writer = csv.writer(csv_file)
        
        # Iterate through each page
        for page_num, page in enumerate(pdf.pages):
            print(f"Processing page {page_num + 1}")
            
            # Find tables in the page
            tables = page.find_tables(table_settings={
                "vertical_strategy": "text",
                "horizontal_strategy": "lines",
                "intersection_tolerance": 5
            })
            
            for table_num, table in enumerate(tables):
                data = table.extract()
                for row in data:
                    # Replace newline characters with a space
                    row = [cell.replace('\n', ' ') for cell in row]
                    print(row)
                    csv_writer.writerow(row)  # Write each row to the CSV file


    print('Processing completed. The table data has been saved to "transactions1.csv".')
    return csv_path

# Path to the PDF file
pdf_file_path = 'DOC-20250101-WA0023..pdf'  # Corrected file path

# Path to the output CSV file
csv_file_path = 'transactions_functionTest.csv'

work = uploadPDF(pdf_file_path,csv_file_path)
print(work)
#################################################################################################
# st.title("Hello, Streamlit!")
# st.write("Welcome to your first Streamlit app.")
# st.text_input("Enter your name:")
