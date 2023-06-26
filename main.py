from web3 import Web3
from typing import Optional
from hexbytes import HexBytes

# https://polygon.llamarpc.com
# https://polygon-mainnet.rpcfast.com?api_key=xbhWBI1Wkguk8SNMu1bvvLurPGLXmgwYeC4S6g2H7WdwFigZSmPWVZRxrskEQwIf
# https://rpc-mainnet.maticvigil.com
# https://1rpc.io/matic
# https://matic-mainnet.chainstacklabs.com
# https://polygon-mainnet-public.unifra.io
# https://rpc.ankr.com/polygon
# https://poly-rpc.gateway.pokt.network
# https://polygon.blockpi.network/v1/rpc/public
# https://rpc-mainnet.matic.quiknode.pro


def transaction_check(txn_hash):
    polygon_rpc_url = 'https://polygon.llamarpc.com'
    web3 = Web3(Web3.HTTPProvider(polygon_rpc_url))


    # txn_hash = '0x53f08bd9ac5e9d387c7306165389c92a21820339b93126f97f8d55265844a931'
    # txn_hash = input('Input transaction hash: ')
    try:
        txn_get = web3.eth.get_transaction(txn_hash) # отсюда нам нужно только кол-во посылаемых монет
        txn_get_receipt = web3.eth.get_transaction_receipt(txn_hash) # отсюда все остальное (от, кому, статус)
        txn_status = ''
        if txn_get_receipt['status'] == 1:
            txn_status = 'Success'
        else:
            txn_status = 'Unsuccess'

        txn_from_address = txn_get_receipt['from']
        txn_to_address = txn_get_receipt['to']
        txn_amount = txn_get['value']
        ether_txn_amount = Web3.from_wei(txn_amount, 'ether')
        # print(f'Is connected: {web3.is_connected()}\n')
        # print(txn_get_receipt)
        # print(txn_receipt['status'])
        # print('Status:', txn_status)
        # print('From:', txn_from_address)
        # print('To:', txn_to_address)
        # print('Amount:', ether_txn_amount, 'MATIC')
        payment_data = f'Status: {txn_status}\n\n' \
                       f'From: {txn_from_address}\n\n' \
                       f'To: {txn_to_address}\n\n' \
                       f'Amount: {ether_txn_amount} MATIC'

        payment_data_and_status = [txn_status, payment_data]
        # return txn_status
        return payment_data_and_status
    except Exception as TransactionNotFound:
        return 'Sorry, transaction not found!'




