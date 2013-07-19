#!/usr/bin/env python
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

printer.text('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
printer.text('abcdefghijklmnopqrstuvwxyz')
printer.text('0123456789')