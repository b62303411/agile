import requests


# Read file and push lines to REST API
def push_lines_to_api(file_path, api_url):
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines into a list

        # Skip the first line (title line)
        lines = lines[1:]

        for line in lines:
            # Assuming each line in the file represents a transaction entry
            transaction_data = line.strip().split(';')  # Assuming CSV format

            # Prepare the data to send to the REST API
            payload = {
                'date': transaction_data[0],
                'account': transaction_data[1],
                'description': transaction_data[2],
                'type': transaction_data[3],
                'amount': transaction_data[4]
            }

            # Make a POST request to the REST API
            response = requests.post(api_url, json=payload)

            # Check the response status
            if response.status_code == 200:
                print(f"Successfully pushed transaction: {line.strip()}")
            else:
                print(f"Failed to push transaction: {line.strip()}")
                print(f"Response: {response.text}")


# Example usage
file_path = 'Y:/Documents/9321-0474 QUEBEC INC/2022/Investment/transactions_td.csv'  # Replace with your file path
api_url = 'http://localhost:8080/addManualTransaction'  # Replace with your API endpoint

push_lines_to_api(file_path, api_url)