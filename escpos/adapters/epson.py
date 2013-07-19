#!/usr/bin/python
'''
@author: Mingcai SHEN <archsh@gmail.com>
@organization: FANGZE SYSTEMS
@copyright: Copyright (c) 2013 FANGZE SYSTEMS
@license: GPLv3
'''
from ..core.escpos import Escpos

class EPSON_TM_T81(Escpos):
    SUPPORTED_BARCODES = ('UPC-A','UPC-E','ITF','NW7','CODE93','EAN13','EAN8','CODE39','CODE128')
    SUPPORTED_IMAGE    = True
    CHARS_PER_LINE     = 48

class EPSON_TM_T88(Escpos):
    SUPPORTED_BARCODES = ('EAN13','EAN8','CODE39','CODE128')
    SUPPORTED_IMAGE    = True
    CHARS_PER_LINE     = 48

class EPSON_TM_U288B(Escpos):
    SUPPORTED_BARCODES = []
    SUPPORTED_IMAGE    = False
    CHARS_PER_LINE     = 40

