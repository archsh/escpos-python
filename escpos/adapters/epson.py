#!/usr/bin/python
'''
@author: Mingcai SHEN <archsh@gmail.com>
@organization: FANGZE SYSTEMS
@copyright: Copyright (c) 2013 FANGZE SYSTEMS
@license: GPLv3
'''
from ..core.escpos import Escpos

class EPSON_POS_Printer(Escpos):
    pass


class EPSON_TM_T81(EPSON_POS_Printer):
    SUPPORTED_BARCODES = ('UPC-A','UPC-E','ITF','NW7','CODE93','EAN13','EAN8','CODE39','CODE128')
    SUPPORTED_IMAGE    = True

class EPSON_TM_T88(EPSON_POS_Printer):
    SUPPORTED_BARCODES = ('UPC-A','UPC-E','ITF','NW7','CODE93','EAN13','EAN8','CODE39','CODE128')
    SUPPORTED_IMAGE    = True

class EPSON_TM_U288B(EPSON_POS_Printer):
    SUPPORTED_BARCODES = []
    SUPPORTED_IMAGE    = False

