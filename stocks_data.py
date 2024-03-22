import json
from Stock import request_json


info = request_json(endpoint='/data/companies.json')
for symbol,data  in info.items():
    if any([data['name'].__contains__('Share'),
            data['name'].__contains__('Promoter'), 
           data['name'].__contains__('Fund'),
           data['name'].__contains__('Debenture'),
           data['name'].__contains__('Yojana'),
           data['name'].__contains__('Kosh'),
           data['name'].__contains__('Trust'),
           data['name'].__contains__('Bond'),
           any(item.isdigit() for item in data['name']),
           ]):
        data['trade'] = False
    else: 
        data['trade'] = True

with open('stocks.json','w') as f:
    json.dump(info,f,indent=4)