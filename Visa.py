import csv
import re
import time
from builtins import bool
from re import Pattern

import numpy as np
import pandas as pd
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import PyPDF2
import csv
import pdfplumber
import os
import requests

# Test the import by printing the library version
print("pdfplumber version:", pdfplumber.__version__)
class DataIntegrity:
    def __init__(self):
        self.top_found = False
        self.date_found = False
        self.bottom_found = False
        self.right_crop_found = False
        self.there_is_another_page = False

class Box:
    def __init__(self):
        self.left = 40
        # With headers 175
        # Without headers 200
        self.top = 200
        self.right_crop = 360
        self.bottom_crop = 500

    def __str__(self):
        return f'Box(left={self.left}, top={self.top}, right_crop={self.right_crop}, bottom_crop={self.bottom_crop})'

class ScanResult:
    def __init__(self):
        self.data_integrity = None
        self.cropped_page = None
        self.table = None

class Visa:
    def __init__(self):
        breakpoint()
    def sendToRest(fileName, api_endpoint, column_names, row):
        for item in row:
            if 'MONTANTNETDEL' in item or 'TOTALNOUVEAUSOLDE' in item:
                #summary statement no need to send
                return

        # PLAN_AFFAIRES_DE_BASE_TD_511-5235425_Jun_30-Jul_30_2021
        pattern = "^([A-Za-z_]+)_(\d{4})_([A-Za-z]{3}_\d{2})-(\d{4})$"
        match = re.match(pattern, fileName)
        if match:
            account_name = match.group(1)
            acc = match.group(2)
            date_report = match.group(3)
            year = match.group(4)

        transaction = dict(zip(column_names, row))
        if(len(transaction['DATE_ACTIVITE'])>6):
            full_str = transaction['DATE_ACTIVITE']
            spaced = full_str.split(' ')
            if(len(spaced)==2):
                transaction['DATE_ACTIVITE'] = spaced[0]
                transaction['DATE_OPERATION'] = spaced[1]
                transaction['DESCRIPTION'] = row[1]
                transaction['MONTANT'] = row[2]
            elif(len(spaced)==4):
                transaction['DATE_ACTIVITE'] = spaced[0]
                transaction['DATE_OPERATION'] = spaced[1]
                transaction['DESCRIPTION'] = spaced[2]
                transaction['MONTANT'] = spaced[3]
            else:
                print("")
                return

        transaction['year'] = year
        transaction['acc'] = acc
        transaction['date_report'] = date_report
        transaction['account_name'] = account_name

        response = requests.post(api_endpoint, json=transaction)

        if response.status_code == 200:
            print("Transaction sent successfully:", transaction)
        else:
            print("Failed to send transaction:", transaction)

    def convertToImage(cropped_page):
        #time.sleep(1)
        print("convert to image")
        print("cropped: width" + str(cropped_page.width) + " Height:" + str(cropped_page.height))
        cropped_image = cropped_page.to_image(resolution=300)
        print("image done")
        #time.sleep(1)
        return cropped_image

    def evaluateRow(row, data_integrity):
        if len(row) > 2:
            data_integrity.date_found = True

        for cell in row:
            print("cell..." + str(cell))
            if not data_integrity.right_crop_found and "$" in cell:
                print("right_crop_found")
                data_integrity.right_crop_found = True
            if data_integrity.right_crop_found and not data_integrity.bottom_found:
                if "Suite" in cell:
                    data_integrity.there_is_another_page = True
                    data_integrity.bottom_found = True
                    print("there_is_another_page")
                    break
                if "MONTANTNETDEL'ACTIVITÉ" in cell or "Suite" in cell:
                    data_integrity.bottom_found = True
                    print("bottom_found")
                    break
        return data_integrity

    def crop(page, box):
        print("crop:" + str(box))
        cropped_page = page.crop((box.left, box.top, box.right_crop, box.bottom_crop))
        print("cropped: width"+str(cropped_page.width)+" Height:"+str(cropped_page.height))
        return cropped_page

    def search_dataframe(df, search_term):
        return df[df.apply(lambda row: row.astype(str).str.contains(search_term).any(), axis=1)]

    def scanSample(box, page, payment_slip_height, table_settings, total_page):
        result = ScanResult()
        data_integrity = DataIntegrity()
        column_names = ['DATE_ACTIVITE', 'DATE_OPERATION', 'DESCRIPTION', 'MONTANT']
        cropped_page = None
        df_clean = None

        # Lets find the upper  Limit
        starting_up = 10
        top_probe = Box()
        while starting_up < page.height-payment_slip_height:


        while box.right_crop < page.width and box.bottom_crop < (page.height-payment_slip_height):
            # Crop the page incrementally
            cropped_page = Visa.crop(page,box)
            #cropped_image = Visa.convertToImage(cropped_page)
            #fileName = "Y:/Documents/9321-0474 QUEBEC INC/" + "TEST"+str(box) + "_" + str(page.page_number) + ".png"
            #cropped_image.save(fileName,
            #                   "PNG", quality=90)
            print("extract_table")
            #time.sleep(1)
            table = cropped_page.extract_table(table_settings)
            print("table extracted")
            #time.sleep(1)
            if table:
                num_columns = len(table[0])
                if num_columns == 4:
                    data_integrity.right_crop_found = True
                    # Convert the table to a pandas DataFrame
                    df = pd.DataFrame(table[0:], columns=column_names)
                    df.replace("", np.nan, inplace=True)
                    df_clean = df.dropna(how='any')
                else:
                    if (page.page_number == 2 or page.page_number == 4):
                        print("Theses pages are usually empy lets skipp")
                        result.data_integrity = data_integrity
                        result.cropped_page = cropped_page
                        result.table = df_clean
                        return result
                    if page.page_number == 1:
                        print("the first page should never be problematic lets fix it.")
                        table_settings = {
                            'vertical_strategy': 'text',
                            'horizontal_strategy': 'text',
                        }
                        table = cropped_page.extract_table(table_settings)
                        num_columns = len(table[0])
                        if(num_columns <= 2):
                            pass_one_row = table[1]
                            test_row = test_text.split(" ")
                            if len(test_row) == 4:
                                df_clean = pd.DataFrame(columns=column_names)
                            else:
                                box.top = 190
                                box.bottom_crop = 230
                                cropped_page = Visa.crop(page, box)
                                text = cropped_page.extract_text()
                                split_text = text.split("\n")
                                for test_text in split_text:
                                    test_row = test_text.split(" ")
                                    if(len(test_row)==4):
                                        df_clean = pd.DataFrame(columns=column_names)
                                        df_clean.loc[len(df_clean)] = test_row
                                        data_integrity.date_found = True
                                        data_integrity.bottom_found = True
                                        data_integrity.right_crop_found = True
                                        result.data_integrity = data_integrity
                                        result.cropped_page = cropped_page
                                        result.table = df_clean
                                        return result



                            print("wdf")

                    print("error")


                contains = Visa.search_dataframe(df,"MONTANTNETDEL'ACTIVITÉ")
                if len(contains) > 0:
                    data_integrity.bottom_found = True
                contains = Visa.search_dataframe(df, "$")
                if len(contains) > 0:
                    data_integrity.right_crop_found = True

                if data_integrity.right_crop_found and data_integrity.bottom_found:
                    result.data_integrity = data_integrity
                    result.cropped_page = cropped_page
                    result.table = df_clean
                    return result

                mask = df.applymap(lambda x: "MONTANTNETDEL'ACTIVITÉ" in str(x))
                contains_tom = mask.any().any()
                if contains_tom:
                    data_integrity.bottom_found = True

                print("iterating table:"+str(len(df)))
                for index, row in df.iterrows():
                    print("row...")
                    data_integrity = Visa.evaluateRow(row, data_integrity)
                    if data_integrity.bottom_found:
                        break

            else:
                print("Table is null:"+str(page.page_number))
                if(page.page_number == 2 or page.page_number == 4):
                    print("Theses pages are usually empy lets skipp")
                    result.data_integrity = data_integrity
                    result.cropped_page = cropped_page
                    result.table = None
                    return result
                elif page.page_number == 3 and total_page == 3:
                    print("If this is the last page lets skip")
                    result.data_integrity = data_integrity
                    result.cropped_page = cropped_page
                    result.table = None
                    return result

            # If no $ found in table, increase the right and bottom crop for the next iteration
            if not data_integrity.right_crop_found:
                    box.right_crop += 10
            elif data_integrity.right_crop_found and not data_integrity.bottom_found:
                    box.bottom_crop += 20
            elif data_integrity.date_found:
                result.data_integrity = data_integrity
                result.cropped_page = cropped_page
                return result
            else:
                table_settings = {
                        'vertical_strategy': 'line',
                        'horizontal_strategy': 'text',
                    }
        result.data_integrity = data_integrity
        result.cropped_page = cropped_page
        result.table = df_clean
        return result
    def scanPage(page,table_settings,total_page):
        print("scanPage")
        # Initial crop settings
        box = Box()
        payment_slip_height = 250
        print(str(box))
        print("Width: "+str(page.width)+" height: "+str(page.height))

        result = Visa.scanSample(box, page, payment_slip_height,table_settings,total_page)
        print(result.data_integrity.date_found)  # prints: False
        if result.data_integrity.right_crop_found:
            cropped_image = Visa.convertToImage(result.cropped_page)
            return result.table, cropped_image
        print("No record found:"+str(page.page_number))
        return None, None

    def handlePage(page,file_name,table_settings,total_page):
        print("handlePage")
        # Define the bounding box. These numbers are just placeholders
        # and you should replace them with your own coordinates.
        print(file_name+"_"+str(page.page_number))
        table, cropped_image = Visa.scanPage(page, table_settings,total_page)
        #time.sleep(1)
        if table is not None:
            try:
                #time.sleep(1)
                cropped_image.save("Y:/Documents/9321-0474 QUEBEC INC/" + file_name +"_"+str(page.page_number)+".png", "PNG", quality=90)
                #time.sleep(1)
                Visa.publishTransaction(table, file_name)
            except Exception:
               print("")
        else:
            return None
        #time.sleep(1)

    def publishTransaction(table,file_name):
        column_names = ['DATE_ACTIVITE', 'DATE_OPERATION', 'DESCRIPTION', 'MONTANT']
        # Find the column indices based on column names
        api_endpoint = "http://localhost:8080/addCreditCardTransaction"
        for index, row in table.iterrows():
            #time.sleep(1)
            print("Send to Rest")
            Visa.sendToRest(file_name, api_endpoint, column_names, row)
            #time.sleep(1)

    def writeToCsv(csv_path,column_names,table):
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)

            for row in table[2:]:  # Skip the header row
                writer.writerow(row)
                if (row[0] == ''):
                    break;
            file.flush();

    def convertToCsv(file_name, pdf_path, csv_path):
        with pdfplumber.open(pdf_path) as pdf:
            table_settings = {
                'vertical_strategy': 'lines',
                'horizontal_strategy': 'text',
            }
            if len(pdf.pages) > 1:
                    print("ca marche!")# Assuming you want to extract data from the first page
            for page in pdf.pages:
                Visa.handlePage(page , file_name,table_settings,len(pdf.pages))
                #time.sleep(1)

    def getAllPdfs(folder_path):
        pdf_files = [os.path.join(filename) for filename in os.listdir(folder_path) if
                         filename.endswith('.pdf')]
        return pdf_files

    def parsePath(folder_path):

        pdf_pairs = Visa.getAllPdfs(folder_path)
        pdf_pairs_list = list(pdf_pairs)
        for filename in pdf_pairs_list:
            name = os.path.splitext(filename)[0]
            pdf_file = os.path.join(folder_path, filename)
            csv_file = os.path.join(folder_path, f'{name}.csv')
            #time.sleep(1)
            try:
                Visa.convertToCsv(name, pdf_file, csv_file)
            except Exception as e:
                print("Error:"+filename+str(e))


# folder_path = 'Y:/Documents/9321-0474 QUEBEC INC/2021/TD/'
base_folder_path = 'Y:/Documents/9321-0474 QUEBEC INC/{}/VISA/'

for year in range(2018, 2024):  # 2024 to include 2023
    folder_path = base_folder_path.format(year)
    Visa.parsePath(folder_path)
# pdf_file = 'PLAN_AFFAIRES_DE_BASE_TD_511-5235425_Feb_26-Mar_31_2021.pdf'
# Iterate over PDF files in the folder
