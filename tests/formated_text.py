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
from escpos.adapters.epson import EPSON_TM_T81, EPSON_TM_T88, EPSON_TM_U288B
TEXTS=u"""
<B>     鼎融食府     </B>
              欢迎您！              


<B>      结算单      </B>
台号：                     T2001
单号：             XS130625-0002

花生酱             3碟  单价：  1.00
    小计：    3.00    折后：    3.00
商务套餐1         -2份  单价： 83.00
    小计： -166.00    折后： -166.00
                  合计：      953.00
              折后合计：      953.00
                服务费：       95.00
              总计应付：     1048.00
BARCODE("XS130625-0002","CODE128",2,98)
------------------------------------
地址：  罗湖区 仙台路1号        
电话：  +86 755 2582 5432       
------------------------------------
             谢谢惠顾！             
QRCODE("XS130625-0002",8,0,1)
"""
#printer = EPSON_TM_U288B(interfaces.Serial(devfile='COM4',baudrate=9600))
printer = EPSON_TM_T81(interfaces.Network('172.20.1.81'))
#printer = Zonerich_AB_88V(interfaces.Network('172.20.1.80'))
#printer.font(font='A',width=2,height=2)
printer.text_formatted(TEXTS,codec='gbk')
#printer.barcode('12345678912','CODE128',width=2,height=70)
#printer.text('0123456789')
printer.cut(n=0)