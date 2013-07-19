#!/usr/bin/python
'''
@author: Mingcai SHEN <archsh@gmail.com>
@organization: FANGZE SYSTEMS
@copyright: Copyright (c) 2013 FANGZE SYSTEMS
@license: GPLv3
'''
from ..core.escpos import Escpos

class ZonerichPrinter(Escpos):
    CODE128_TYPE       = None
    SUPPORTED_BARCODES = ('EAN13','EAN8','CODE39','CODE128')
    SUPPORTED_IMAGE    = True
    CHARS_PER_LINE     = None
    BARCODE_PREFIX     = '\x1b\x61\x00'

class Zonerich_AB_58C(ZonerichPrinter):
    CHARS_PER_LINE     = 36

class Zonerich_AB_88V(ZonerichPrinter):
    CHARS_PER_LINE     = 48


