import json
import requests
from datetime import datetime

base_url = "https://github.com/the-value-crew/nepse-api/tree/master"

class Stock:
    def __init__(self,symbol):
        self.symbol = symbol.upper()
        self.id, self.name = self.company()
        self.file = f"data/{self.symbol.replace('/','∕')}.csv"
    
    def __call__(self):
        return self.symbol

    def company(self):
        endpoint = "/data/companies.json"
        data = request_json(endpoint)[self.symbol]
        return data["id"],data["name"]
    
    def get_data(self,start_date=None,end_date=None):
        endpoint = f"/data/company/{self.symbol.replace('/','∕')}.json"
        data = request_json(endpoint)
        
        if not start_date and not end_date:
            return data
        
        if not end_date:
            if not isinstance(start_date, datetime):start_date = datetime.strptime(start_date, '%Y-%m-%d')
            return {date: values for date, values in data.items() if start_date <= datetime.strptime(date, '%Y-%m-%d')}

        if not start_date:
            if not isinstance(end_date, datetime):end_date = datetime.strptime(end_date, '%Y-%m-%d')
            return {date: values for date, values in data.items() if datetime.strptime(date, '%Y-%m-%d') <= end_date}

        if not isinstance(start_date, datetime):start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if not isinstance(end_date, datetime):end_date = datetime.strptime(end_date, '%Y-%m-%d')
        return {date: values for date, values in data.items() if start_date <= datetime.strptime(date, '%Y-%m-%d') <= end_date}

def request_json(endpoint):
    url = base_url + endpoint
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.json()["payload"]["blob"]["rawLines"][0])
    else:
        print("Error",response.status_code,f" in {url}")

def dump(data):
    with open("dump.json",'w') as f:
        json.dump(data,f,indent=4)

if __name__ == '__main__':
    stock = Stock("akjcl")
    print(stock.name)
    dump(stock.get_data(start_date='2024-1-1',end_date='2024-3-10'))