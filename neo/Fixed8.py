# -*- coding:utf-8 -*-
"""
Description:
    Fixed8
Usage:
    from neo.Fixed8 import Fixed8
"""


from decimal import Decimal as D
from neo.Helper import big_or_little


class Fixed8:



    """docstring for Fixed8"""
    def __init__(self, number):
        self.f = D(str(number))

    def getData(self):
        hex_str = hex(int(self.f*D('100000000')))[2:]
        if len(hex_str)%2:
            hex_str = '0' + hex_str
        return big_or_little(hex_str)

    @staticmethod
    def Satoshi():
        return Fixed8(1)