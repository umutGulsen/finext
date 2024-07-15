import requests
import os
from evds import evdsAPI
evds_api_key = os.environ.get('EVDS_API')
def test():
    print("TEST")
    evds_url = 'https://evds2.tcmb.gov.tr/service/evds/'
    #session = requests.Session()
    #request = session.get(evds_url + params, headers={'key': self.key})

    print(evds_api_key)
    evds = evdsAPI(evds_api_key)
    print(evds.main_categories)
    subs = evds.get_sub_categories(2)
    print(subs.iloc[:,1])
    series = evds.get_series("bie_dkdovytl")
    print(series)
    data = evds.get_data(['TP.DK.USD.A.YTL', 'TP.DK.EUR.A.YTL'], startdate="01-01-2024")
    print(data)


def main():
    pass

if __name__ == '__main__':
    main()