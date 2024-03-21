import json
import requests

base_url = "https://github.com/the-value-crew/nepse-api/tree/master"

class Stock:
    def __init__(self,symbol):
        self.symbol = symbol.upper()
        self.id, self.name = self.company()

    def company(self):
        endpoint = "/data/companies.json"
        data = request_json(endpoint)[self.symbol]
        return data["id"],data["name"]
    
    def get_data(self,date=None):
        endpoint = f"/data/company/{self.symbol.replace('/','∕')}.json"
        data = request_json(endpoint)
        if not date:
            return data
        return data[date]

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
