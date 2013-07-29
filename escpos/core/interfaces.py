#!/usr/bin/python
'''
@author: Manuel F Martinez <manpaz@bashlinux.com>
@organization: Bashlinux
@copyright: Copyright (c) 2012 Bashlinux
@license: GPL
'''

#import usb.core
#import usb.util
import serial
import socket

from . import exceptions

class Interface(object):
    """
    Abstract class of interfaces.
    """
    def _write(self, msg):
        raise exceptions.DeviceError(msg='Use the instance of Interface is now allowed!')
    def _writable(self):
        return True
    def _readable(self):
        return True
    
    

class Usb(Interface):
    """ Define USB printer """

    def __init__(self, idVendor, idProduct, interface=0, in_ep=0x82, out_ep=0x01):
        """
        @param idVendor  : Vendor ID
        @param idProduct : Product ID
        @param interface : USB device interface
        @param in_ep     : Input end point
        @param out_ep    : Output end point
        """
        self.idVendor  = idVendor
        self.idProduct = idProduct
        self.interface = interface
        self.in_ep     = in_ep
        self.out_ep    = out_ep
        self.open()



    def open(self):
        """ Search device on USB tree and set is as escpos device """
        self.device = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)
        if self.device is None:
            print "Cable isn't plugged in"

        if self.device.is_kernel_driver_active(0):
            try:
                self.device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                print "Could not detatch kernel driver: %s" % str(e)

        try:
            self.device.set_configuration()
            self.device.reset()
        except usb.core.USBError as e:
            print "Could not set configuration: %s" % str(e)
    
    def _read(self, n=None):
        return self.device.read()
    

    def _write(self, msg):
        """ Print any command sent in raw format """
        self.device.write(self.out_ep, msg, self.interface)


    def __del__(self):
        """ Release USB interface """
        if self.device:
            usb.util.dispose_resources(self.device)
        self.device = None



class Serial(Interface):
    """ Define Serial printer """

    def __init__(self, devfile="/dev/ttyS0", baudrate=9600, bytesize=8, timeout=1, dsrdtr=False,rtscts=False,xonxoff=False,stopbits=serial.STOPBITS_TWO,parity=serial.PARITY_NONE):
        """
        @param devfile  : Device file under dev filesystem
        @param baudrate : Baud rate for serial transmission
        @param bytesize : Serial buffer size
        @param timeout  : Read/Write timeout
        """
        self.devfile  = devfile
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.timeout  = timeout
        self.dsrdtr   = dsrdtr
        self.xonxoff  = xonxoff
        self.stopbits = stopbits
        self.parity   = parity
        self.rtscts   = rtscts
        self.open()
    
    def _writable(self):
        if self.dsrdtr or self.rtscts:
            return self.device.getDSR()
        return True
    
    def _readable(self):
        if self.dsrdtr or self.rtscts:
            return self.device.getDSR()
        return True


    def open(self):
        """ Setup serial port and set is as escpos device """
        self.device = serial.Serial(port=self.devfile, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, timeout=self.timeout, rtscts=self.rtscts, dsrdtr=self.dsrdtr,xonxoff=self.xonxoff)
        if self.device is not None and self.device.writable():
            pass #print "Serial printer enabled"
        else:
            print "Unable to open serial printer on: %s" % self.devfile

    def _read(self, n=1):
        if not self.device or not self.device.readable():
            raise Exception("Can not read serial.")
        return self.device.read(size=n)
    
    
    def _write(self, msg):
        """ Print any command sent in raw format """
        if not self.device or not self.device.writable():
            raise Exception("Can not write serial.")
        self.device.write(msg)


    def __del__(self):
        """ Close Serial interface """
        if self.device is not None:
            self.device.close()



class Network(Interface):
    """ Define Network printer """

    def __init__(self,host,port=9100,timeout=5.0):
        """
        @param host : Printer's hostname or IP address
        @param port : Port to write to
        """
        self.host = host
        self.port = port
        self.open(timeout=timeout)


    def open(self,timeout=5.0):
        """ Open TCP socket and set it as escpos device """
        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device.settimeout(timeout)
        self.device.connect((self.host, self.port))
        if self.device is None:
            print "Could not open socket for %s" % self.host

    def _read(self, n=None):
        return self.device.recv(4096 if n is None else n,0)

    def _write(self, msg):
        self.device.send(msg)

    def __del__(self):
        """ Close TCP connection """
        self.device.close()
