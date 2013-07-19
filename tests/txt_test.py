#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: Mingcai SHEN <archsh@gmail.com>
@organization: FANGZE SYSTEMS
@copyright: Copyright (c) 2013 FANGZE SYSTEMS
@license: GPLv3
'''
import sys
sys.path.append('../')

from escpos.core import escpos, interfaces
from escpos.adapters.zonerich import Zonerich_AB_88V

#printer = escpos.Escpos(interfaces.Serial(devfile='COM4',baudrate=9600))
printer = Zonerich_AB_88V(interfaces.Network('172.20.1.80'))
#printer.font(font='A',width=2,height=2)
printer.text(u'ABCDEFGHI\n共产党\nJKLMNOPQRSTUVWXYZ'.encode('gbk'))
printer.text(u'abcdefghi中国jklmno\npqrstuvwxyz'.encode('gbk'))
printer.barcode('12345678912','CODE128',width=2,height=70)
#printer.text('0123456789')
printer.cut(n=0)