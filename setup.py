#!/usr/bin/env python

from distutils.core import setup
from escpos import __version__
setup(name='escpos-python',
      version=__version__,
      description='Yet another implementation of ESC/POS library for ESC/POS Printers base on Juliano Bittencourt\'s original version.',
      author='Mingcai SHEN, Juliano Bittencourt',
      author_email='archsh@gmail.com,juliano@hardfunstudios.com',
      url='https://github.com/archsh/escpos-python',
      packages=['escpos','escpos.adapters','escpos.core'],
      requires=[
          "pyserial (>= 2.5)",
          "pyusb (>= 1.0)",
          "PIL (>= 1.1.7)",
      ],
     )