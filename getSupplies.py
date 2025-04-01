import requests
import urllib3
import json
from getParams import getParams
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getSupplies(ip):
    try:      
        supplies = {}
        params = getParams(ip)
        match params['Brand']:
            case 'Konica':
                supplies['Brand'] = params['Brand']
                supplies['Counter'] = params['Counter']
                response = requests.get(params['Url'], headers=params['Header'], cookies=params['Cookies'], verify=False)
                if response.status_code == 200:
                    json_supplies = json.loads(response.text)
                    groups = {}
                    for consumable in json_supplies['MFP']['ConsumableList']['Consumable']:
                        if consumable['Type'] not in groups:
                            groups[consumable['Type']] = [consumable]
                        else:
                            groups[consumable['Type']].append(consumable)

                    for type in groups:
                        if type not in supplies: supplies[type] = []
                        for item in groups[type]:
                            if 'WasteTonerBottle' in type:
                                supplies[type].append({'Name': item['Name'], 'State': item['CurrentLevel']['LevelState']})
                            else:
                                supplies[type].append({'Name': item['Name'], 'Percent': item['CurrentLevel']['LevelPer'], 'State': item['CurrentLevel']['LevelState']})
                supplies['IP'] = ip
                supplies['Status'] = 'Online'
                return supplies
            
            case 'Brother':
                return params
        
    except:
        return {'Status': 'Offline', 'IP': ip}