escpos-python
=============

Yet another implementation of ESC/POS library for ESC/POS Printers base on Juliano Bittencourt's original version(See: https://github.com/jbittencourt/python-escpos).

ESCPOS from Juliano Bittencourt
======

Python library to manipulate ESC/POS Printers.

------------------------------------------------------------------
1. Dependencies

In order to start getting access to your printer, you must ensure
you have previously installed the following python modules:

  * pyusb (python-usb)
  * PIL (Python Image Library)

------------------------------------------------------------------
2. Description

Python ESC/POS is a library which lets the user have access to all
those printers handled by ESC/POS commands, as defined by Epson,
from a Python application.

The standard usage is send raw text to the printer, but in also 
helps the user to enhance the experience with those printers by
facilitating the bar code printing in many different standards,
as well as manipulating images so they can be printed as brand
logo or any other usage images migh have. 

Text can be aligned/justified and fonts can be changed by size,
type and weight.

Also, this module handles some hardware functionalities like, cut
paper, carrier return, printer reset and others concerned to the
carriage alignment.

------------------------------------------------------------------
3. Define your printer

Before start create your Python ESC/POS printer instance, you must
see at your system for the printer parameters. This is done with
the 'lsusb' command.

First run the command to look for the "Vendor ID" and "Product ID",
then write down the values, these values are displayed just before
the name of the device with the following format:

  xxxx:xxxx

Example:
  Bus 002 Device 001: ID 1a2b:1a2b Device name

Write down the the values in question, then issue the following
command so you can get the "Interface" number and "End Point"

  lsusb -vvv -d xxxx:xxxx | grep iInterface
  lsusb -vvv -d xxxx:xxxx | grep bEndpointAddress | grep OUT

The first command will yields the "Interface" number that must
be handy to have and the second yields the "Output Endpoint"
address.

By default the "Interface" number is "0" and the "Output Endpoint"
address is "0x82",  if you have other values then you can define
with your instance.

------------------------------------------------------------------
4. Define your instance

The following example shows how to initialize the Epson TM-TI88IV
*** NOTE: Always finish the sequence with Epson.cut() otherwise
          you will endup with weird chars being printed.

  from escpos import *

  """ Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
  Epson = escpos.Escpos(0x04b8,0x0202,0)
  Epson.text("Hello World")
  Epson.image("logo.gif")
  Epson.barcode
  Epson.barcode('1324354657687','EAN13',64,2,'','')
  Epson.cut()

------------------------------------------------------------------

5. Setup International Page Codes

The following example sets the printer page code to Portuguese (cp860). 

  from escpos import *

  Epson = escpos.Escpos(0x04b8,0x0202,0)
  Epson.setPageCode(constants.CP_PORTUGUESE)

Currently supported page codes are:

	CP_ENGLISH - PC437 (USA: Standard Europe)
	CP_KATAKANA - Katakana
	CP_MULTILINGUAL - PC850 (Multilingual)
	CP_PORTUGUESE - [PC860 (Portuguese)]
	CP_FRENCH - PC863 (Canadian-French)
	CP_NORDIC - PC865 (Nordic)
	CP_WINDOWS - WPC1252
	CP_CYRILLIC - PC866 (Cyrillic #2)
	CP_LATIN2 - PC852 (Latin 2)
	CP_EURO - PC858 (Euro)

If your printer support a different code page, you can send the command directly to the printer. 

Command is written in the format :  ESC t n , where n stands for the printer code for the code page 
	
	from escpos import *
	CUSTOM_CODEPAGE = '\x1b\x74\x24'  # \x1b\x74 stands for ESC t
	
	Epson = escpos.Escpos(0x04b8,0x0202,0)
	Epson.setPageCode(CUSTOM_CODEPAGE)
	
In this case it is very important to setup the encoding which escpos will use to send strings to the printer. You can do this by:

	Epson.setOutputEncoding(customEncoding)
	
For a list of available encodings, visit http://docs.python.org/library/codecs.html

------------------------------------------------------------------
6. Links


Fork with support for international code pages added by

Juliano Bittencourt <juliano.bittencourt@gmail.com>

https://github.com/jbittencourt/python-escpos


Original Code by 

Manuel F Martinez <manpaz@bashlinux.com>

Please visit project homepage at:
http://repo.bashlinux.com/projects/escpos.html
