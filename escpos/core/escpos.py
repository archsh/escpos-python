#!/usr/bin/env python
'''
@author: Manuel F Martinez <manpaz@bashlinux.com>
@organization: Bashlinux
@copyright: Copyright (c) 2012 Bashlinux
@license: GPL
'''

import Image
import time
import re
import qrcode

from exceptions import *
from . import interfaces
from . import commands


BARCODE_REGEX=r'BARCODE\(\"(?P<value>[A-Z0-9a-z-_]+)\"\,\"(?P<bc>[A-Z0-9]+)\"\,(?P<width>[0-9]+)\,(?P<height>[0-9]+)\)'
QRCODE_REGEX=r'QRCODE\(\"(?P<value>[A-Z0-9a-z-_]+)\"\,(?P<size>[0-9]+)\,(?P<border>[0-9]+)\,(?P<version>[0-9]+)\)'
CONTROL_REGEX=r'CONTROL\(\"(?P<value>[A-Z0-9a-z-_]+)\"\)'
TAB_REGEX=r'TAB\((?P<value>[0-9,]+)\)'

def transcode_unicode(val,codec='utf8'):
    if isinstance(val,str):
        return unicode(val,codec)
    elif isinstance(val,(list,tuple)):
        return [transcode_unicode(x) for x in val]
    elif isinstance(val,dict):
        return dict([(k,transcode_unicode(v,codec)) for k,v in val.items()])
    else:
        return val

def regex_to_list(txt,regex,type):
    pt = re.compile(regex)
    texts=list()
    start=0
    end=0
    if not isinstance(txt,(str,unicode)):
        return txt
    for m in pt.finditer(txt):
        s,e = m.span()
        texts.append(txt[start:s])
        start=e
        texts.append((type,m.groupdict()))
    else:
        texts.append(txt[start:])
    return texts

def gen_qrcode_data(code,size=4, border=0, version=1):
    f = cStringIO.StringIO()
    qr = qrcode.QRCode(version=version, box_size=size, border=border)
    qr.add_data(code)#('order://5d2738f8-782a-11e2-9a10-000c29a7c6dc/pay')
    qr.make(fit=True)
    x = qr.make_image().save(f,'png')
    return '<img align="center" src="data:image/png;base64,%s">'%base64.b64encode(f.getvalue())

def gen_barcode_data(code, bc, width, height, pos='BELOW', font='A'):
    from restbooks.core import barcode
    from restbooks.core.barcode.writer import ImageWriter
    f = cStringIO.StringIO()
    print 'width:',width
    print 'height:',height
    if bc.lower() in barcode.PROVIDED_BARCODES:
        BARCODE = barcode.get_barcode_class(bc.lower())
        gen = BARCODE(code, writer=ImageWriter())
        gen.render({'write_text':False,'module_width':width/15.0,'module_height':height/25.0,'quiet_zone':0.5}).save(f,'png')
        return '<img align="center" src="data:image/png;base64,%s">'%base64.b64encode(f.getvalue())
    else:
        return ''
    #return '<img src="data:image/png;base64,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">'



def deflat_list(lst):
    ret = list()
    for x in lst:
        if isinstance(x,list):
            for y in deflat_list(x):
                ret.append(y)
        else:
            ret.append(x)
    return ret

class Escpos(object):
    """ ESC/POS Printer object """
    SUPPORTED_BARCODES = []
    SUPPORTED_IMAGE    = False
    CODE128_TYPE       = '{A'
    BARCODE_PREFIX     = '\x1b\x61\x01'
    #device    = None
    
    """ ESC/POS Commands (Constants) """

    # Feed control sequences
    CTL_LF    = '\x0a'             # Print and line feed
    CTL_FF    = '\x0c'             # Form feed
    CTL_CR    = '\x0d'             # Carriage return
    CTL_HT    = '\x09'             # Horizontal tab
    CTL_VT    = '\x0b'             # Vertical tab
    # Printer hardware
    HW_INIT   = '\x1b\x40'         # Clear data in buffer and reset modes
    HW_SELECT = '\x1b\x3d\x01'     # Printer select
    HW_RESET  = '\x1b\x3f\x0a\x00' # Reset printer hardware
    # Cash Drawer
    CD_KICK_2 = '\x1b\x70\x00'     # Sends a pulse to pin 2 [] 
    CD_KICK_5 = '\x1b\x70\x01'     # Sends a pulse to pin 5 [] 
    # Paper
    PAPER_FULL_CUT  = '\x1d\x56\x00' # Full cut paper
    PAPER_PART_CUT  = '\x1d\x56\x01' # Partial cut paper
    # Text format   
    TXT_NORMAL      = '\x1b\x21\x00\x1c\x21\x00' # Normal text
    TXT_2HEIGHT     = '\x1b\x21\x10\x1c\x21\x08' # Double height text
    TXT_2WIDTH      = '\x1b\x21\x20\x1c\x21\x04' # Double width text
    TXT_2SIZE       = '\x1b\x21\x30\x1c\x21\x0c' # Double width and height text
    TXT_UNDERL_OFF  = '\x1b\x2d\x00\x1c\x2d\x00' # Underline font OFF
    TXT_UNDERL_ON   = '\x1b\x2d\x01\x1c\x2d\x01' # Underline font 1-dot ON
    TXT_UNDERL2_ON  = '\x1b\x2d\x02\x1c\x2d\x02' # Underline font 2-dot ON
    TXT_BOLD_OFF    = '\x1b\x45\x00' # Bold font OFF
    TXT_BOLD_ON     = '\x1b\x45\x01' # Bold font ON
    TXT_FONT_A      = '\x1b\x4d\x00' # Font type A
    TXT_FONT_B      = '\x1b\x4d\x01' # Font type B
    TXT_FONT_C      = '\x1b\x4d\x02' # Font type C
    TXT_ALIGN_LT    = '\x1b\x61\x00' # Left justification
    TXT_ALIGN_CT    = '\x1b\x61\x01' # Centering
    TXT_ALIGN_RT    = '\x1b\x61\x02' # Right justification
    # Barcode format
    BARCODE_TXT_OFF = '\x1d\x48\x00' # HRI barcode chars OFF
    BARCODE_TXT_ABV = '\x1d\x48\x01' # HRI barcode chars above
    BARCODE_TXT_BLW = '\x1d\x48\x02' # HRI barcode chars below
    BARCODE_TXT_BTH = '\x1d\x48\x03' # HRI barcode chars both above and below
    BARCODE_FONT_A  = '\x1d\x66\x00' # Font type A for HRI barcode chars
    BARCODE_FONT_B  = '\x1d\x66\x01' # Font type B for HRI barcode chars
    BARCODE_HEIGHT  = '\x1d\x68\x64' # Barcode Height [1-255]
    BARCODE_WIDTH   = '\x1d\x77\x03' # Barcode Width  [2-6]
    BARCODE_TYPES   = {
        'UPC-A': commands.GS_6b_m_n+chr(65),
        'UPC-E': commands.GS_6b_m_n+chr(66),
        'EAN13': commands.GS_6b_m_n+chr(67),
        'EAN8': commands.GS_6b_m_n+chr(68),
        'CODE39': commands.GS_6b_m_n+chr(69),
        'ITF': commands.GS_6b_m_n+chr(70),
        'CODABAR': commands.GS_6b_m_n+chr(71),
        'NW7': commands.GS_6b_m_n+chr(71),
        'CODE93': commands.GS_6b_m_n+chr(72),
        'CODE128': commands.GS_6b_m_n+chr(73),
    }
    # Image format  
    S_RASTER_N      = '\x1d\x76\x30\x00' # Set raster image normal size
    S_RASTER_2W     = '\x1d\x76\x30\x01' # Set raster image double width
    S_RASTER_2H     = '\x1d\x76\x30\x02' # Set raster image double height
    S_RASTER_Q      = '\x1d\x76\x30\x03' # Set raster image quadruple

    def __init__(self, intfs):
        """
        (intfs)-> An interface instance should be provided.
        """
        assert isinstance(intfs,interfaces.Interface)
        self.device = intfs
        self._write = intfs._write
        self._read  = intfs._read
        for tp in self.SUPPORTED_BARCODES:
            if tp not in self.BARCODE_TYPES:
                raise Error('Invalid SUPPORTED_BARCODES!')
        self.initialize()
        
    def initialize(self):
        self._write(commands.ESC_40)
        self._write(commands.ESC_53)
    
    def check_available(self,flag=True):
        self._write(commands.DLE_04_n+chr(1))
        ret = self._read(n=1)
        if not ret:
            raise DeviceError(msg='Printer No Response.')
        print '1.Ret: ','-'.join(['{0:08b}'.format(ord(x)) for x in ret])
        ret = ord(ret[0])
        if flag and ret&0x08:
            # Printer Off Line
            raise DeviceError(msg='Printer Off Line.')
        self._write(commands.DLE_04_n+chr(4))
        ret = self._read(n=1)
        print '4.Ret: ','-'.join(['{0:08b}'.format(ord(x)) for x in ret])
        ret = ord(ret[0])
        if flag and ret&0x6c:
            raise DeviceError(msg='Printer Paper Out.')

    

    def _check_image_size(self, size):
        """ Check and fix the size of the image to 32 bits """
        if size % 32 == 0:
            return (0, 0)
        else:
            image_border = 32 - (size % 32)
            if (image_border % 2) == 0:
                return (image_border / 2, image_border / 2)
            else:
                return (image_border / 2, (image_border / 2) + 1)


    def _print_image(self, line, size):
        """ Print formatted image """
        i = 0
        cont = 0
        buffer = ""
        output = list()
       
        output.append(self.S_RASTER_N)
        buffer = "%02X%02X%02X%02X" % (((size[0]/size[1])/8), 0, size[1], 0)
        output.append(buffer.decode('hex'))
        buffer = ""

        while i < len(line):
            hex_string = int(line[i:i+8],2)
            buffer += "%02X" % hex_string
            i += 8
            cont += 1
            if cont % 4 == 0:
                output.append(buffer.decode("hex"))
                buffer = ""
                cont = 0
        if output:
            self._write(''.join(output))

    def image_raw(self,img_raw):
        """Print an Image object"""
        if not self.SUPPORTED_IMAGE:
            return
        pixels   = []
        pix_line = ""
        im_left  = ""
        im_right = ""
        switch   = 0
        img_size = [ 0, 0 ]
        im = img_raw.convert("RGB")
        if im.size[0] > 512:
            print  "WARNING: Image is wider than 512 and could be truncated at print time "
        if im.size[1] > 255:
            raise ImageSizeError()

        im_border = self._check_image_size(im.size[0])
        for i in range(im_border[0]):
            im_left += "0"
        for i in range(im_border[1]):
            im_right += "0"

        for y in range(im.size[1]):
            img_size[1] += 1
            pix_line += im_left
            img_size[0] += im_border[0]
            for x in range(im.size[0]):
                img_size[0] += 1
                RGB = im.getpixel((x, y))
                im_color = (RGB[0] + RGB[1] + RGB[2])
                im_pattern = "1X0"
                pattern_len = len(im_pattern)
                switch = (switch - 1 ) * (-1)
                for x in range(pattern_len):
                    if im_color <= (255 * 3 / pattern_len * (x+1)):
                        if im_pattern[x] == "X":
                            pix_line += "%d" % switch
                        else:
                            pix_line += im_pattern[x]
                        break
                    elif im_color > (255 * 3 / pattern_len * pattern_len) and im_color <= (255 * 3):
                        pix_line += im_pattern[-1]
                        break 
            pix_line += im_right
            img_size[0] += im_border[1]

        self._print_image(pix_line, img_size)

    def image(self, img):
        """ Parse image and prepare it to a printable format """
        if not self.SUPPORTED_IMAGE:
            return
        im_open = Image.open(img)
        self.image_raw(im_open)

    def qr_code(self,code,size=4, border=0, version=1):
        if not code:
            return
        qr = qrcode.QRCode(version=version, box_size=size, border=border)
        qr.add_data(code)#('order://5d2738f8-782a-11e2-9a10-000c29a7c6dc/pay')
        qr.make(fit=True)
        x = qr.make_image()._img
        self.image_raw(x)
    
    def barcode(self, code, bc, width=98, height=2, pos='OFF', font='A'):
        """ Print Barcode """
        if not self.SUPPORTED_BARCODES:
            return
        elif bc not in self.SUPPORTED_BARCODES:
            return
        output = list()
        # Align Bar Code()
        if self.BARCODE_PREFIX:
            output.append(self.BARCODE_PREFIX)
        # Height
        if height >=2 or height <=6:
            output.append(self.BARCODE_HEIGHT)
        else:
            raise BarcodeSizeError()
        # Width
        if width >= 1 or width <=255:
            output.append(self.BARCODE_WIDTH)
        else:
            raise BarcodeSizeError()
        # Font
        if font.upper() == "B":
            output.append(self.BARCODE_FONT_B)
        else: # DEFAULT FONT: A
            output.append(self.BARCODE_FONT_A)
        # Position
        if pos.upper() == "OFF":
            output.append(self.BARCODE_TXT_OFF)
        elif pos.upper() == "BOTH":
            output.append(self.BARCODE_TXT_BTH)
        elif pos.upper() == "ABOVE":
            output.append(self.BARCODE_TXT_ABV)
        else:  # DEFAULT POSITION: BELOW 
            output.append(self.BARCODE_TXT_BLW)
        # Type
        if bc.upper() in self.SUPPORTED_BARCODES:
            output.append(self.BARCODE_TYPES[bc.upper()])
            
        else:
            raise BarcodeTypeError()
        # Print Code
        if code:
            if bc.upper() == 'CODE128':
                if self.CODE128_TYPE:
                    #print 'Add: ',self.CODE128_TYPE
                    code = ''.join([self.CODE128_TYPE,code])
            code_length = len(code)
            if bc.upper() == "EAN13" and (code_length<12 or code_length>13):
                raise exception.BarcodeCodeError()
            elif bc.upper() == "EAN8" and (code_length<7 or code_length>8):
                raise exception.BarcodeCodeError()
            elif bc.upper() == "CODE39" and (code_length<1 or code_length>255):
                raise exception.BarcodeCodeError()
            elif bc.upper() == "CODE128" and (code_length<2 or code_length>255):
                raise exception.BarcodeCodeError()
            output.append(chr(code_length))
            
            output.append(code)
        else:
            raise exception.BarcodeCodeError()
        if output:
            self._write(''.join(output))

    def text(self, txt):
        """ Print alpha-numeric text """
        if txt:
            self._write(txt)
    
    def font(self, font='A',type='NORMAL',width=1,height=1):
        output = list()
        if font and font.upper() == "C":
            output.append(self.TXT_FONT_C)
        elif font and font.upper() == "B":
            output.append(self.TXT_FONT_B)
        else:  # DEFAULT FONT: A
            output.append(self.TXT_FONT_A)
        # Type
        if type is not None:
            if type.upper() == "B":
                output.append(self.TXT_BOLD_ON)
                output.append(self.TXT_UNDERL_OFF)
            elif type.upper() == "U":
                output.append(self.TXT_BOLD_OFF)
                output.append(self.TXT_UNDERL_ON)
            elif type.upper() == "U2":
                output.append(self.TXT_BOLD_OFF)
                output.append(self.TXT_UNDERL2_ON)
            elif type.upper() == "BU":
                output.append(self.TXT_BOLD_ON)
                output.append(self.TXT_UNDERL_ON)
            elif type.upper() == "BU2":
                output.append(self.TXT_BOLD_ON)
                output.append(self.TXT_UNDERL2_ON)
            elif type.upper == "NORMAL":
                output.append(self.TXT_BOLD_OFF)
                output.append(self.TXT_UNDERL_OFF)
        # Width
        if width is not None and height is not None:
            if width == 2 and height != 2:
                output.append(self.TXT_NORMAL)
                output.append(self.TXT_2WIDTH)
            elif height == 2 and width != 2:
                output.append(self.TXT_NORMAL)
                output.append(self.TXT_2HEIGHT)
            elif height == 2 and width == 2:
                output.append(self.TXT_2SIZE)
                #output.append(self.TXT_2HEIGHT)
            else: # DEFAULT SIZE: NORMAL
                output.append(self.TXT_NORMAL)
        if output:
            self._write(''.join(output))
    
    def align(self, align=None):
        # Align
        if align is not None:
            if align.upper() == "CENTER":
                self._write(self.TXT_ALIGN_CT)
            elif align.upper() == "RIGHT":
                self._write(self.TXT_ALIGN_RT)
            elif align.upper() == "LEFT":
                self._write(self.TXT_ALIGN_LT)
        else:
            output.append(self.TXT_ALIGN_LT)

    def cut(self, mode='',n=None):
        """ Cut paper """
        # Fix the size between last line and cut
        # TODO: handle this with a line feed
        #self._write("\n\n\n\n")
        self._write(commands.LF)
        if n is not None:
            if mode.upper() == "PART":
                c = commands.GS_56_m+chr(66)+chr(n)
            else: # DEFAULT MODE: FULL CUT
                c = commands.GS_56_m+chr(65)+chr(n)
        else:
            if mode.upper() == "PART":
                c = commands.GS_56_m+chr(1)
            else: # DEFAULT MODE: FULL CUT
                c = commands.GS_56_m+chr(0)
        self._write(c)


    def cashdraw(self, pin=2):
        """ Send pulse to kick the cash drawer """
        if pin == 2:
            self._write(self.CD_KICK_2)
        elif pin == 5:
            self._write(self.CD_KICK_5)
        else:
            raise CashDrawerError()


    def hw(self, hw):
        """ Hardware operations """
        if hw.upper() == "INIT":
            self._write(self.HW_INIT)
        elif hw.upper() == "SELECT":
            self._write(self.HW_SELECT)
        elif hw.upper() == "RESET":
            self._write(self.HW_RESET)
        else: # DEFAULT: DOES NOTHING
            pass


    def control(self, ctl):
        """ Feed control sequences """
        if ctl.upper() == "LF":
            self._write(self.CTL_LF)
        elif ctl.upper() == "FF":
            self._write(self.CTL_FF)
        elif ctl.upper() == "CR":
            self._write(self.CTL_CR)
        elif ctl.upper() == "HT":
            self._write(self.CTL_HT)
        elif ctl.upper() == "VT":
            self._write(self.CTL_VT)
            
    @classmethod
    def format(klass,txt):
        #output = ''.join([x.strip() for x in txt.split('\n')])
        output = txt.replace('<B>',klass.TXT_2SIZE).replace('</B>',klass.TXT_NORMAL)\
               .replace('<W>',klass.TXT_2WIDTH).replace('</W>',klass.TXT_NORMAL)\
               .replace('<H>',klass.TXT_2HEIGHT).replace('</H>',klass.TXT_NORMAL) \
               .replace('<HT>',klass.CTL_HT).replace('<CR>',klass.CTL_LF)\
               .replace('<L>',commands.ESC_61_n+chr(0)).replace('<C>',commands.ESC_61_n+chr(1)).replace('<R>',commands.ESC_61_n+chr(2))
        return output
    
    def text_formatted(self, txt, codec="gbk"):
        texts = deflat_list([regex_to_list(x,QRCODE_REGEX,'QRCODE') for x in regex_to_list(txt,BARCODE_REGEX,'BARCODE')])
        texts = deflat_list([regex_to_list(x,CONTROL_REGEX,'CONTROL') for x in texts])
        texts = deflat_list([regex_to_list(x,TAB_REGEX,'TAB') for x in texts])
        
        #print texts
        #self._write(commands.ESC_4c)
        for x in texts:
            if isinstance(x,(str,unicode)):
                x = x.encode('gbk')
                self.text(self.format(x))
            elif isinstance(x,tuple):
                if x[0]=='BARCODE':
                    self.barcode(x[1]['value'],x[1]['bc'],int(x[1]['width']),int(x[1]['height']))
                elif x[0]=='QRCODE':
                    self.qr_code(x[1]['value'],int(x[1]['size']),int(x[1]['border']),int(x[1]['version']))
                elif x[0]=='CONTROL':
                    self.control(x[1]['value'])
                elif x[0]=='TAB':
                    tabs = [int(n) for n in x[1]['value'].split(',')]
                    if tabs:
                        self._write(commands.ESC_44+''.join(map(lambda x:chr(x), tabs))+chr(0))
            else:
                pass
        self._write(commands.LF)
