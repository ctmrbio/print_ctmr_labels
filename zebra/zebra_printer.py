__author__ = "Fredrik Boulund"
__date__ = "2017"
__doc__ = """Simple Zebra printer object."""

import socket 
import time
import logging

logger = logging.getLogger(__name__)

class zebra_printer():
    """
    Zebra printer object.
    """

    def __init__(self, tcp_ip, tcp_port):
        """
        Initialize a Zebra printer object.

        Tries to open a connection to verify the printer is operational.
        Logs an error if connection cannot be established. 
        """
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        try:
            s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            s.connect((self.tcp_ip, self.tcp_port))
        except ConnectionRefusedError:
            logger.error("Connection to %s:%s refused." % self.tcp_ip, self.tcp_port)
        finally:
            s.close()

    def send_to_zebra(self, payload):
        """
        Send payload to printer.

        The printer expects ZPL code.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.tcp_ip, self.tcp_port))
        time.sleep(1)
        response = s.send(payload)
        time.sleep(1)
        s.close()
        return response

    def test_print(self):
        """
        Send test label to Zebra printer.
        
        Should print a simple label with some text and a bar code:
            TEST PRINT
             |||||||
        """
        test_zpl = "^XA^CF0,60^FO10,10^FDTEST PRINT^FS^FO60,50^B8,20,10^FD6000133^FS^XZ"
        logger.info('Sending code: {}'.format(test_zpl))
        r = self.send_to_zebra(test_zpl)
        logger.info('Printer response: {}'.format(r))
