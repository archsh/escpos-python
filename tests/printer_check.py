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

from escpos.core import escpos, interfaces, commands
from escpos.adapters.zonerich import Zonerich_AB_88V
from escpos.adapters.epson import EPSON_TM_T81, EPSON_TM_T88, EPSON_TM_U288B

#printer = EPSON_TM_U288B(interfaces.Serial(devfile='COM4',baudrate=9600))
#printer = Zonerich_AB_88V(interfaces.Network('172.20.1.80'))
printer = EPSON_TM_T81(interfaces.Network('172.20.1.81'))
#printer._write(commands.DLE_04_n+chr(4))
#ret = printer._read()
#print 'Ret: {0:08b}'.format(ord(ret))
printer.check_available(False)
#printer.font(font='A',width=2,height=2)
#printer.text(u'ABCDEFGHI共产党JKLMNOPQRSTUVWXYZ'.encode('gbk'))
#printer.text(u'abcdefghi中国jklmnopqrstuvwxyz'.encode('gbk'))
#printer.barcode('12345678912','CODE39',width=100,height=3)
#printer.text('0123456789')
#printer.cut(n=5)