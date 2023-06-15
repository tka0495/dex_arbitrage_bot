# import asyncio
# from bscscan import BscScan
#
# YOUR_API_KEY = "NCV1T3QM2I1DUBBMT2YNIG5Q8W41U64GI9"
#
# async def main():
#   async with BscScan(YOUR_API_KEY) as bsc:
#     print(await bsc.get_bnb_balance(address="0x0000000000000000000000000000000000001004"))
#
# if __name__ == "__main__":
#   asyncio.run(main())

import requests
from bs4 import BeautifulSoup

url = 'https://polygonscan.com/tx/'
transaction = '0x01b5c920a564fbe5c4351c06fae4a8eea6141dfaf12dc26be7a158ea2f77e6fa'
my_url = url + transaction

response = requests.get(my_url)
bs = BeautifulSoup(response.text, "lxml")
print(response.text)



status_code = bs.find('span', 'u-label u-label--sm u-label--success rounded')
from_to = bs.find('span', 'hash-tag text-truncate hash-tag-custom-from tooltip-address')
to_to = bs.find('span', 'hash-tag text-truncate hash-tag-custom-to tooltip-address')
# print('Статус:', status_code.text)
print('Статус:', status_code)
print('От:', from_to.text)
print('Кому:', to_to.text)
