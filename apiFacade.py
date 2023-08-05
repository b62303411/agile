import re
import requests

class ApiFacade:
    def publishTransaction(table,file_name):
        column_names = ['DATE_ACTIVITE', 'DATE_OPERATION', 'DESCRIPTION', 'MONTANT']
        # Find the column indices based on column names
        api_endpoint = "http://localhost:8080/addCreditCardTransaction"
        for index, row in table.iterrows():
            #time.sleep(1)
            print("Send to Rest")
            ApiFacade.sendToRest(file_name, api_endpoint, column_names, row)
            #time.sleep(1)
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