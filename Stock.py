import json
import requests
from datetime import datetime

base_url = "https://the-value-crew.github.io/nepse-api"
COMPANIES = {'SWMF', 'RNLI', 'GFCL', 'MEL', 'GRDBL', 'PSF', 'KLBSL', 'PBLD84', 'NHPC', 'ALBSL', 'MMKJL', 'UHEWA', 'PPCL', 'MFLD85', 'HIDCLP', 'RBCL', 'DHPL', 'NMFBS', 'SLCF', 'SADBL', 'NICFC', 'AVYAN', 'SHLB', 'RURU', 'UNLB', 'CMF1', 'NLG', 'VLBS', 'NIBD2082', 'CMF2', 'GBILD86/87', 'SPL', 'C30MF', 'LEMF', 'JSLBB', 'SCB', 'BNHC', 'ICFCD83', 'SPC', 'NTC', 'NLICL', 'NADEP', 'NMBMF', 'GUFL', 'BEDC', 'MPFL', 'SBCF', 'IHL', 'LBBL', 'SBID83', 'SHINE', 'HIDCL', 'BHPL', 'UMRH', 'DDBL', 'NIMB', 'BGWT', 'SICL', 'NBLD87', 'MSLB', 'KEF', 'SIKLES', 'SAPDBL', 'NIBD84', 'KBL', 'FOWAD', 'PPL', 'PHCL', 'RMF1', 'NHDL', 'MLBSL', 'WNLB', 'PRIN', 'MSHL', 'JFL', 'NBL', 'VLUCL', 'ADBL', 'MBJC', 'NICGF', 'MLBS', 'RHGCL', 'TRH', 'MHL', 'BNL', 'SHIVM', 'BHDC', 'CITY', 'ENL', 'CHDC', 'LVF2', 'SWMFPO', 'MEN', 'CHL', 'HURJA', 'NGPL', 'HBLD86', 'DLBS', 'SAMAJ', 'LEC', 'SRLI', 'MCHL', 'GILB', 'MLBL', 'NMB', 'JBLB', 'HPPL', 'MHCL', 'NIMBPO', 'EBL', 'SMATA', 'PRVUPO', 'SMH', 'NICSF', 'CKHL', 'SIFC', 'ULHC', 'NRIC', 'TAMOR', 'AKPL', 'SLBBL', 'SBD87', 'HHL', 'PRVU', 'AHPC', 'SMFBS', 'USHL', 'GHL', 'MKCL', 'NLIC', 'BFC', 'BHL', 'RAWA', 'GMFIL', 'SHPC', 'NYADI', 'SWBBL', 'UNHPL', 'SFCL', 'GLBSL', 'API', 'CLI', 'STC', 'CHCL', 'SMJC', 'H8020', 'IGI', 'SHL', 'HATHY', 'AHL', 'NFS', 'FOWADP', 'JBBD87', 'KRBL', 'SSHL', 'SAEF', 'JOSHI', 'RMF2', 'MDB', 'NWCL', 'LSL', 'SGIC', 'NSIF2', 'UMHL', 'USHEC', 'SONA', 'NICL', 'MHNL', 'EHPL', 'SANIMA', 'BARUN', 'NICA', 'KPCL', 'KKHC', 'OHL', 'LUK', 'NRN', 'NBF2', 'DOLTI', 'DORDI', 'MKHC', 'HLBSL', 'HEIP', 'MERO', 'ALICL', 'KSBBLD87', 'GBLBS', 'SARBTM', 'PMHPL', 'MLBBL', 'SGHC', 'NMB50', 'SJCL', 'SBI', 'CFCL', 'RSDC', 'SAHAS', 'SIGS3', 'UAIL', 'SKBBL', 'NABIL', 'PRSF', 'LICN', 'CZBIL', 'NIFRA', 'HEI', 'GIBF1', 'RADHI', 'UPCL', 'RLFL', 'PROFL', 'MMF1', 'SMB', 'KBSH', 'UPPER', 'ICFC', 'TSHL', 'UNL', 'ANLB', 'NICBF', 'MEHL', 'NICGF2', 'SPDL', 'RFPL', 'RIDI', 'ACLBSL', 'CCBD88', 'SPIL', 'GVL', 'NBLD85', 'PBD88', 'NUBL', 'SFEF', 'GBBD85', 'SINDU', 'RBCLPO', 'NESDO', 'SBLD84', 'BNT', 'KDL', 'HRL', 'JBBL', 'KBLPO', 'NIBSF2', 'GBBL', 'EDBL', 'MAKAR', 'PFL', 'MBLD2085', 'CORBL', 'SBID89', 'NMBD87/88', 'BPCL', 'MKLB', 'MBL', 'SRD80', 'ADBLD83', 'SMHL', 'NICD83/84', 'HDHPC', 'SDLBSL', 'KMCDB', 'MKHL', 'HBL', 'NIL', 'BOKD86', 'NBF3', 'ILBS', 'RHPL', 'PMLI', 'TPC', 'MNBBL', 'CIT', 'SDBD87', 'BBC', 'USLB', 'HDL', 'NIBLGF', 'SEF', 'MFIL', 'JALPA', 'SABSL', 'GBIME', 'SBL', 'FMDBL', 'KDBY', 'ILI', 'NRM', 'GWFD83', 'PCBL', 'NICLBSL', 'CBLD88', 'CGH', 'TVCL', 'MBLPO', 'SHEL', 'SPHL', 'SJLIC', 'SALICO', 'GMFBS', 'SNLI', 'PBD85', 'CYCL', 'ULBSL', 'NABBC', 'MANDU', 'HLI', 'KSBBL', 'CBBL', 'GCIL', 'LLBS', 'GLH', 'SAGF', 'AKJCL', 'SIGS2'}
with open("stocks.json",'r') as f:
    info = json.load(f)

class Stock:
    def __init__(self,symbol):
        self.symbol = symbol.upper()
        self.id = info[self.symbol]['id']
        self.name = info[self.symbol]['name']
        self.trade = info[self.symbol]['trade']
        self.file = f"data/{self.symbol.replace('/','∕')}.csv"
    
    def __call__(self):
        return self.symbol
    
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
        return response.json()
        print("Error",response.status_code,f" in {url}")

def dump(data):
    with open("dump.json",'w') as f:
        json.dump(data,f)

if __name__ == '__main__':
    endpoint = '/data/companies.json'
    data = request_json(endpoint)
    print(data)
