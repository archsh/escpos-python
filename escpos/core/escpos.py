#!/usr/bin/python
'''
@author: Manuel F Martinez <manpaz@bashlinux.com>
@organization: Bashlinux
@copyright: Copyright (c) 2012 Bashlinux
@license: GPL
'''

import Image
import time

from constants import *
from exceptions import *

class Escpos(object):
    """ ESC/POS Printer object """
    device    = None
    
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
    TXT_NORMAL      = '\x1b\x21\x00' # Normal text
    TXT_2HEIGHT     = '\x1b\x21\x10' # Double height text
    TXT_2WIDTH      = '\x1b\x21\x20' # Double width text
    TXT_UNDERL_OFF  = '\x1b\x2d\x00' # Underline font OFF
    TXT_UNDERL_ON   = '\x1b\x2d\x01' # Underline font 1-dot ON
    TXT_UNDERL2_ON  = '\x1b\x2d\x02' # Underline font 2-dot ON
    TXT_BOLD_OFF    = '\x1b\x45\x00' # Bold font OFF
    TXT_BOLD_ON     = '\x1b\x45\x01' # Bold font ON
    TXT_FONT_A      = '\x1b\x4d\x00' # Font type A
    TXT_FONT_B      = '\x1b\x4d\x01' # Font type B
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
    BARCODE_UPC_A   = '\x1d\x6b\x00' # Barcode type UPC-A
    BARCODE_UPC_E   = '\x1d\x6b\x01' # Barcode type UPC-E
    BARCODE_EAN13   = '\x1d\x6b\x02' # Barcode type EAN13
    BARCODE_EAN8    = '\x1d\x6b\x03' # Barcode type EAN8
    BARCODE_CODE39  = '\x1d\x6b\x04' # Barcode type CODE39
    BARCODE_ITF     = '\x1d\x6b\x05' # Barcode type ITF
    BARCODE_NW7     = '\x1d\x6b\x06' # Barcode type NW7
    # Image format  
    S_RASTER_N      = '\x1d\x76\x30\x00' # Set raster image normal size
    S_RASTER_2W     = '\x1d\x76\x30\x01' # Set raster image double width
    S_RASTER_2H     = '\x1d\x76\x30\x02' # Set raster image double height
    S_RASTER_Q      = '\x1d\x76\x30\x03' # Set raster image quadruple


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
            self._raw(''.join(output))


    def image(self, img):
        """ Parse image and prepare it to a printable format """
        pixels   = []
        pix_line = ""
        im_left  = ""
        im_right = ""
        switch   = 0
        img_size = [ 0, 0 ]

        im_open = Image.open(img)
        im = im_open.convert("RGB")

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


    def barcode(self, code, bc, width, height, pos, font):
        """ Print Barcode """
        output = list()
        # Align Bar Code()
        output.append(self.TXT_ALIGN_CT)
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
        if bc.upper() == "UPC-A":
            output.append(self.BARCODE_UPC_A)
        elif bc.upper() == "UPC-E":
            output.append(self.BARCODE_UPC_E)
        elif bc.upper() == "EAN13":
            output.append(self.BARCODE_EAN13)
        elif bc.upper() == "EAN8":
            output.append(self.BARCODE_EAN8)
        elif bc.upper() == "CODE39":
            output.append(self.BARCODE_CODE39)
        elif bc.upper() == "ITF":
            output.append(self.BARCODE_ITF)
        elif bc.upper() == "NW7":
            output.append(self.BARCODE_NW7)
        else:
            raise BarcodeTypeError()
        # Print Code
        if code:
            output.append(code)
        else:
            raise exception.BarcodeCodeError()
        if output:
            self._raw(''.join(output))

        
    def text(self, txt):
        """ Print alpha-numeric text """
        if txt:
            self._raw(txt)
        else:
            raise TextError()


    def set(self, align=None, font=None, type=None, width=None, height=None):
        """ Set text properties """
        output = list()
        # Align
        if align is not None:
            if align.upper() == "CENTER":
                output.append(self.TXT_ALIGN_CT)
            elif align.upper() == "RIGHT":
                output.append(self.TXT_ALIGN_RT)
            elif align.upper() == "LEFT":
                output.append(self.TXT_ALIGN_LT)
        # Font
        if font is not None:
            if font.upper() == "B":
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
                output.append(self.TXT_2WIDTH)
                output.append(self.TXT_2HEIGHT)
            else: # DEFAULT SIZE: NORMAL
                output.append(self.TXT_NORMAL)
        
        if output:
            self._raw(''.join(output))


    def cut(self, mode=''):
        """ Cut paper """
        # Fix the size between last line and cut
        # TODO: handle this with a line feed
        self._raw("\n\n\n\n")
        if mode.upper() == "PART":
            self._raw(self.PAPER_PART_CUT)
        else: # DEFAULT MODE: FULL CUT
            self._raw(self.PAPER_FULL_CUT)


    def cashdraw(self, pin=2):
        """ Send pulse to kick the cash drawer """
        if pin == 2:
            self._raw(self.CD_KICK_2)
        elif pin == 5:
            self._raw(self.CD_KICK_5)
        else:
            raise CashDrawerError()


    def hw(self, hw):
        """ Hardware operations """
        if hw.upper() == "INIT":
            self._raw(self.HW_INIT)
        elif hw.upper() == "SELECT":
            self._raw(self.HW_SELECT)
        elif hw.upper() == "RESET":
            self._raw(self.HW_RESET)
        else: # DEFAULT: DOES NOTHING
            pass


    def control(self, ctl):
        """ Feed control sequences """
        if ctl.upper() == "LF":
            self._raw(self.CTL_LF)
        elif ctl.upper() == "FF":
            self._raw(self.CTL_FF)
        elif ctl.upper() == "CR":
            self._raw(self.CTL_CR)
        elif ctl.upper() == "HT":
            self._raw(self.CTL_HT)
        elif ctl.upper() == "VT":
            self._raw(self.CTL_VT)
