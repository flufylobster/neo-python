#!/usr/bin/env python
"""
Description:
    IndexedDBWallet
Usage:
    from neo.Implementations.Wallets.IndexedDBWallet import IndexedDBWallet
"""

from neo.Defaults import BlockChainDB
from neo.Implementations.Wallets.DbContext import Mongodb
from neo.Wallets.Coin import Coin
from neo.Wallets.CoinState import CoinState
from neo.Core.AssetType import *

class IndexedDBWallet():
    def __init__(self):
        self.mongo = Mongodb(host=BlockChainDB.host, port=BlockChainDB.port)

    def findCoins(self, address, status=None):
        if status:
            qry = {'address': address, 'status': status}
        else:
            qry = {'address': address}
        items = self.mongo.read('coins', qry)
        coins = []
        for i in items:
            c = Coin(txid=i['txid'], idx = i['idx'], value=i['value'], asset=i['asset'],
                     address=i['address'], status=i['status'])
            coins.append(c)
        return coins

    def findAssetByName(self, name, status="Registed"):
        qry = {'name': name, 'status': status}
        items = self.mongo.read('asset', qry)
        if len(items)>0:
            return items[0]
        return None

    def loadCoins(self, address, asset):
        qry = {'address': address, 'asset':asset, 'status': CoinState.Unspent}
        items = self.mongo.read('coins', qry)
        coins = []
        for i in items:
            c = Coin(txid=i['txid'], idx = i['idx'], value=i['value'], asset=i['asset'],
                     address=i['address'], status=i['status'])
            coins.append(c)
        return coins

    def onSendTransaction(self, spending, incoming):
        for c in spending:
            qry = {'txid':c.txid,'idx':c.idx}
            self.mongo.update('coins', qry,{'$set':{'status':CoinState.Spending}})
        for c in incoming:
            qry = {'txid':c.txid,'idx':c.idx}
            item = {}
            item['txid'] = c.txid
            item['idx'] = c.idx
            item['value'] = c.value
            item['address'] = c.address
            item['asset'] = c.asset
            item['status'] = CoinState.Unconfirmed
            self.mongo.replace('coins', qry, item)

    def queryAccount(self, work_id):
        qry = {'work_id': work_id}
        items = self.mongo.read('account', qry)
        if len(items)>0:
            return items[0]
        return None

def __test():
    address = 'Adpd2LoUndjEWvdRVrk4SDnAAJ9hM2GgYP'
    wallet = IndexedDBWallet()
    coins = wallet.loadCoins(address, AssetType.AntShare)
    print(coins)

if __name__ == '__main__':
    __test()
