import csv
import re
from re import Pattern

import PyPDF2
import csv
import pdfplumber
import os
import requests

# Test the import by printing the library version
print("pdfplumber version:", pdfplumber.__version__)


def sendToRest(fileName, api_endpoint, column_names, row):
    # PLAN_AFFAIRES_DE_BASE_TD_511-5235425_Jun_30-Jul_30_2021
    pattern = "^([A-Za-z_]+)_(\d{3}-\d{7})_([A-Za-z]{3}_\d{2})-([A-Za-z]{3}_\d{2})_(\d{4})$"
    match = re.match(pattern, fileName)
    if match:
        account_name = match.group(1)
        account_info = match.group(2)
        suc = account_info.split('-')[0]
        acc = account_info.split('-')[1]
        date_from = match.group(3)
        date_to = match.group(4)
        year = match.group(5)
    else :
        account_name = fileName[0:24]
        suc = fileName[25:28]
        acc = fileName[29:36]
        date_from = fileName[37:43]
        date_to = fileName[44:50]
        year = fileName[51:55]
    transaction = dict(zip(column_names, row))
    transaction['year'] = year;
    transaction['suc'] = suc
    transaction['acc'] = acc
    transaction['date_from'] = date_from
    transaction['date_to'] = date_to

    response = requests.post(api_endpoint, json=transaction)

    if response.status_code == 200:
        print("Transaction sent successfully:", transaction)
    else:
        print("Failed to send transaction:", transaction)


def convertToCsv(file_name, pdf_path, csv_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]  # Assuming you want to extract data from the first page
        table_settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
        }
        table = page.extract_table(table_settings)
        column_names = ['DESCRIPTION', 'RETRAITS', 'DEPOTS', 'DATE', 'SOLDE']
        # Find the column indices based on column names
        api_endpoint = "http://localhost:8080/addTransaction"
        for row in table[2:]:
            sendToRest(file_name, api_endpoint, column_names, row)

        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)

            for row in table[2:]:  # Skip the header row
                writer.writerow(row)
                if (row[0] == ''):
                    break;
            file.flush();


def parsePath(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            # Extract the name without the extension
            name = os.path.splitext(filename)[0]

            # Path to the PDF file
            pdf_file = os.path.join(folder_path, filename)

            # Path to the CSV file
            csv_file = os.path.join(folder_path, f'{name}.csv')
            convertToCsv(name, pdf_file, csv_file)


# folder_path = 'Y:/Documents/9321-0474 QUEBEC INC/2021/TD/'
base_folder_path = 'Y:/Documents/9321-0474 QUEBEC INC/{}/TD/'

for year in range(2018, 2024):  # 2024 to include 2023
    folder_path = base_folder_path.format(year)
    parsePath(folder_path)
# pdf_file = 'PLAN_AFFAIRES_DE_BASE_TD_511-5235425_Feb_26-Mar_31_2021.pdf'
# Iterate over PDF files in the folder
