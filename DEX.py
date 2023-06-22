import datetime
from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
import time
import os

# ПОДКЛЮЧЕНИЕ К API (СТАНДАРТНОЕ)
CREDENTIALS_FILE = '/Users/default/Desktop/Projects/DEX-bot/credentials.json'
spreadsheet_id = '16hZdiEzBCxmf8TjQZuLfPQCLJ-a-xCdxeTJmGnTX7oE'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive']
)
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


# ФУНКЦИЯ ПРЕОБРАЗОВАНИЯ ПРОЧИТАННОЙ ИНФОРМАЦИИ ИЗ ТАБЛИЦЫ В УДОБНЫЙ ВИД ДЛЯ ВЫВОДА
def transform(data_dict, key=True):
    if key:
        data_dict = data_dict.get('values')[0][0].split('\n')
        return data_dict
    else:
        data_dict = data_dict.get('values')[0][0]
        return data_dict


# ФУНКЦИЯ ЧТЕНИЯ ИНФОРМАЦИИ ИЗ ГУГЛ ТАБЛИЦЫ
def read_data_from_sheets(cell, id=spreadsheet_id, method='COLUMNS'):
    read_data = service.spreadsheets().values().get(
        spreadsheetId=id,
        range=cell,
        majorDimension=method,
    ).execute()
    return read_data


# ФУНКЦИЯ ПОИСКА ИНФОРМАЦИИ О ПОКУПКЕ/ПРОДАЖЕ ПО ЗАДАННЫМ ПАРАМЕТРАМ (МОНЕТЫ ПОК/ПРОД)
def buy_and_sale(counter, alphabet_dict, bid_cells, sell_cells, data):
    # data = []
    bid_info = read_data_from_sheets(bid_cells)
    sell_info = read_data_from_sheets(sell_cells)
    # dex_exchanges = ['UniswapV..', 'Balancer', '0x Protocol', '0xProtoc..', '1Inch',
    #                  'Sushiswap..', 'SushiSwa..', 'SushiSwap', 'Sushiswa..', 'ApeSwap',
    #                  'Pancake..', 'MDEX(HE..', 'Quickswa..']
    dex_exchanges = ['SushiSwap', 'Sushiswa..', 'Sushiswap..', 'SushiSwa..',
                     '0x Protocol', '0xProtoc..', '1Inch', 'ApeSwap',
                     'Pancake Swap', 'Pancake..'] #'Biswap' 'Mdex (BSC)', 'Dodo (BSC)'
    coins_change = ['USDT', 'USDC', 'WBNB', 'BTC', 'WETH', 'ETH', 'DAI']
    # coins_change = ['USDT', 'USDC', 'BTC']
    for i in range(12):
        bid_str = bid_info.get('values')[0][i].split(
            '\n')  # Чтение информации об одной покупке (0-Биржа, 1-Цена, 3-Пара)
        bid_coin = bid_str[3].split('/')  # Парсинг второй монеты в паре (напр. DAI/USDT, спарсится отсюда - USDT)
        if bid_str[0] in dex_exchanges and bid_coin[
            1] in coins_change:  # Условие для поиска и отбора необходимых бирж и пар
            for j in range(12):
                sell_str = sell_info.get('values')[j][0].split('\n')
                print("SELL_STR = ", sell_str)
                our_coin = sell_str[3].split('/')
                if sell_str[0] in dex_exchanges and our_coin[1] in coins_change:
                    index_spread_cell = str(alphabet_dict[j + 1]) + str(counter + i)  # ВЫЧИСЛЕНИЕ ЯЧЕЙКИ СО СПРЕДОМ ПО СТОЛБЦУ И СТРОКЕ
                    spread = transform(read_data_from_sheets(index_spread_cell),
                                              False) # Чтение информации из ячейки и выделение процента спреда
                    print("INDEX_SPREAD = ", index_spread_cell)
                    if len(spread) == 6:
                        spread = float(spread[1:5]) # тестируемое условие чтобы преобразовывало в плавующую точку как
                    elif len(spread) == 5:                           # числа +1.00%, так и числа +3$ и +0.9%
                        spread = float(spread[1:3])
                    else:
                        spread = float(spread[1:2])

                    # if round(spread, 2) >= 1.00 and bid_str[3] != sell_str[3]:
                    # if round(spread, 2) >= 1.3 and bid_str[3] != sell_str[3]: # Исключает ошибки в парах м-ду протоколами
                    if round(spread, 2) >= 1.3:
                        data.append(f'\U00002796\U00002796\U00002796\U00002796'
                                    f'\U00002796\U00002796\U00002796\U00002796\U00002796\n'
                                    f'\U0001F4C8 Покупка: {bid_str[0]}\n\U0001F4B0 Цена: {bid_str[1]}\n\U0001F504 Пара: {bid_str[3]}\n\n'
                                    f'\U0001F4C9 Продажа: {sell_str[0]}\n\U0001F4B0 Цена: {sell_str[1]}\n\U0001F504 Пара: {sell_str[3]}\n\n'
                                    f'\U00002705 Спред: {spread}% \U0001F4B8\n\n\n')
                        # print(i + 1, 'Покупка:', bid_str[0], end=' ')  # биржа
                        # print('Цена:', bid_str[1], end=' ')  # цена
                        # print('Пара:', bid_str[3])  # пара
                        # print(j + 1, 'Продажа:', sell_str[0], end=' ')
                        # print('Цена:', sell_str[1], end=' ')
                        # print('Пара:', sell_str[3])
                        # print('Спред:', spread)
                        # print(data)
                        with open('test.txt', 'a') as f:
                            # svazka_str = str(bid_str + sell_str)
                            svazka_str = str(i + 1) + ' Покупка: ' + str(bid_str[0]) + ' Цена: ' \
                                         + str(bid_str[1]) + ' Пара: ' + str(bid_str[3]) + '\n' + str(j + 1) \
                                         + ' Продажа: ' + str(sell_str[0]) + ' Цена: ' + str(sell_str[1]) \
                                         + ' Пара: ' + str(sell_str[3]) + '\nСпред: ' + str(spread) + '\n\n'
                            f.write('Запись в ' + datetime.datetime.now().strftime("%H:%M:%S  %d.%m.%Y") + '\n')
                            f.write(str(svazka_str) + '\n\n')
                            # print('Файл перезаписан в {}'.format(datetime.datetime.now().strftime("%H:%M:%S  %d.%m.%Y")))
                    # print(i + 1, 'Покупка:', bid_str[0], end=' ')  # биржа
                    # print('Цена:', bid_str[1], end=' ')  # цена
                    # print('Пара:', bid_str[3])  # пара
                    # print(j + 1, 'Продажа:', sell_str[0], end=' ')
                    # print('Цена:', sell_str[1], end=' ')
                    # print('Пара:', sell_str[3])
                    # print('Спред:', spread)
                    # print()
    return data

# ФУНКЦИЯ КОМПОНОВКИ ДЛЯ ВСЕХ МОНЕТ
def aggregator():
    global new_data
    data_test = []
    # info_dict = {'!B2:B13': '!C1:N1', '!B18:B29': '!C17:N17', '!B34:B45': '!C33:N33',
    #              '!B50:B61': '!C49:N49', '!B66:B77': '!C65:N65', '!B82:B93': '!C81:N81',
    #              '!B98:B109': '!C97:N97', '!B114:B125': '!C113:N113', '!B130:B141': '!C129:N129',
    #              '!B146:B157': '!C145:N145', '!B162:B173': '!C161:N161'}
    # ETHEREUM

    info_dict = {'!B114:B125': '!C113:N113', '!B130:B141': '!C129:N129',
                 '!B146:B157': '!C145:N145'} # SPELL APE MKR

    alphabet_cells = {1: 'C', 2: 'D', 3: 'E', 4: 'F', 5: 'G', 6: 'H',
                      7: 'I', 8: 'J', 9: 'K', 10: 'L', 11: 'M', 12: 'N'}

    # count_cells = 2 # ЭТО ЕСЛИ info_dict ИЗНАЧАЛЬНЫЙ
    count_cells = 114
    for index in info_dict:
        new_data = buy_and_sale(count_cells, alphabet_cells, index, info_dict[index], data_test)
        count_cells += 16

    return new_data

# while True:
#     aggregator()
#     time.sleep(60)

# СПИСОК ВАЛИДНЫХ DEX-БИРЖ
eth_dex_exchanges = ['Uniswap V2', 'Uniswap V3', 'Balancer', '0x Protocol', '1Inch', 'SushiSwap', 'ApeSwap',
                     'Bancor Network']
bnb_dex_exchanges = ['SushiSwap', '0x Protocol', 'Biswap', '1Inch', 'ApeSwap', 'Pancake Swap', 'Mdex (BSC)', 'Dodo (BSC)']
polygon_dex_exchanges = ['SushiSwap', 'Balancer', '0x Protocol', '1Inch', 'ApeSwap', 'Quickswap']