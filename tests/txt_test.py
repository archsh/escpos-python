#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: Mingcai SHEN <archsh@gmail.com>
@organization: FANGZE SYSTEMS
@copyright: Copyright (c) 2013 FANGZE SYSTEMS
@license: GPLv3
'''
import sys
#sys.path.append('../')

from escpos.core import escpos, interfaces
from escpos.adapters.zonerich import Zonerich_AB_88V
from escpos.adapters.epson import EPSON_TM_T81, EPSON_TM_T88, EPSON_TM_U288B
TEXTS=u"""
<B>     鼎融食府     </B>
              欢迎您！              
"""
printer = EPSON_TM_U288B(interfaces.Serial(devfile='COM3',baudrate=9600))
#printer = EPSON_TM_T81(interfaces.Network('172.20.1.81'))
#printer = Zonerich_AB_88V(interfaces.Network('172.20.1.80'))
#printer.font(font='A',width=2,height=2)
printer.text(TEXTS.encode('gbk'))
printer.barcode('12345678912','CODE128',width=2,height=70)
#printer.text('0123456789')
printer.cut(n=0)