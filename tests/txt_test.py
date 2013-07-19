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

printer = escpos.Escpos(interfaces.Serial(devfile='COM4',baudrate=9600))
printer.font(font='A',width=2,height=2)
printer.text(u'ABCDEFGHI\n共产党\nJKLMNOPQRSTUVWXYZ'.encode('gbk'))
printer.text(u'abcdefghi中国jklmno\npqrstuvwxyz'.encode('gbk'))
#printer.barcode('12345678912','CODE39',width=100,height=3)
#printer.text('0123456789')
printer.cut(n=5)