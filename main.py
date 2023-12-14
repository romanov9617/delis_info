import os
from datetime import datetime

import requests
import xmltodict
import pandas as pd

URL = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='

def cb_rf_request():
    date = datetime.today().strftime('%d/%m/%Y')
    url = f'{URL}{date}'
    response = requests.get(url)
    currency_dict = xmltodict.parse(response.text)

    for currency in currency_dict['ValCurs']['Valute']:
        currency['Value'] = float(currency['Value'].replace(',', '.'))
        currency['VunitRate'] = float(currency['VunitRate'].replace(',', '.'))
        currency['Nominal'] = int(currency['Nominal'])

    return currency_dict


def main():

    if not os.path.exists('currencies/'):
        os.mkdir('currencies/')
    today_excel = f'currencies/{datetime.today().strftime("%d_%m_%Y")}.xlsx'
    if not os.path.exists(today_excel):
        with pd.ExcelWriter(today_excel, engine='xlsxwriter') as writer:
            df = pd.DataFrame(cb_rf_request()['ValCurs']['Valute'])
            df.to_excel(writer, sheet_name='currencies', index=False)

if __name__ == '__main__':
    main()
