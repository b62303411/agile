import pandas as pd
import requests
import json

# Read the CSV file
df = pd.read_csv('Y:/Documents/9321-0474 QUEBEC INC/2018/transactions.csv')
df = df.fillna("")
# Iterate over each row
for index, row in df.iterrows():
    # Create a dictionary for the current row
    data = {
        'date': row['Date'],
        'description': row['Description'],
        'originalDescription': row['Original Description'],
        'amount': row['Amount'],
        'transactionType': row['Transaction Type'],
        'category': row['Category'],
        'accountName': row['Account Name'],
        'labels': row['Labels'],
    }

    api_url = 'http://localhost:8080/addLegacyTransaction'
    # Send a POST request to the API
    response = requests.post(api_url, json=data)

    # Check the status of the request
    if response.status_code == 200:
        print(f"Row {index} was successfully posted.")
    else:
        print(f"Row {index} failed to post. Response code: {response.status_code}")
