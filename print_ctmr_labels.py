#!/usr/bin/env python2.7
# encoding: utf-8 
from __future__ import print_function
from sys import argv, exit
import socket
import time
import argparse
import logging

from gooey import Gooey

from zebra import zebra_printer
from labels import *

__author__ = "CTMR, Fredrik Boulund"
__date__ = "2017"
__doc__ = """Print labels using Zebra printer."""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@Gooey(program_name="CTMR Zebra label printing application", image_dir="img")
def parse_args():
    """
    Parse command line.
    """

    credit = "Bacteria artwork by Ina Schuppe Koistinen. Zebra icon by FreePik from Flaticon."
    desc = "".join([__doc__, "\nCopyright (c) ", __date__, " ", __author__, ".\n", credit])

    parser = argparse.ArgumentParser(description=desc)
    subparsers = parser.add_subparsers()

    for label in all_labels:
        label_ = label()
        subparser = label_.initialize_subparser(subparsers)

        printer = subparser.add_argument_group("Printer settings")
        printer.add_argument("--copies", '-c', dest="copies",
                type=int,
                default=2,
                help="Number of copies per label.")
        printer.add_argument("--zebra-ip", "-I", dest="zebra_ip",
                default="169.254.133.1",
                help="IP number to Zebra printer.")
        printer.add_argument("--zebra-port", "-P", dest="zebra_port",
                default=9100,
                type=int,
                help="Port number for Zebra printer.")
        printer.add_argument("--zebra-buffer", "-B", dest="zebra_buffer",
                default=1024,
                type=int,
                help="Buffer size for Zebra printer.")
        printer.add_argument("--test", "-T", dest="test_print", action="store_true",
                help="Test print.")
        printer.add_argument("--dryrun", "-Y", dest="dryrun", action="store_true",
                help="Dryrun; do not print anything.")
        printer.add_argument("--cancel", "-C", dest="cancel", action="store_true",
                help="Cancel all jobs.")
            

    return parser.parse_args()


def main(options):
    """
    Main function.
    """

    if not options.dryrun:
        try:
            zebra = zebra_printer(options.zebra_ip, options.zebra_port)
        except IOError:
            exit(2)

    if options.cancel:
        zebra.cancel_jobs()
        exit()

    selected_label = options.func()
    payload = selected_label.make_labels(options)

    if options.dryrun:
        print(payload)
        return "Dryrun; nothing sent to printer."

    if options.test_print:
        zebra.test_print()
        exit()

    response = zebra.send_to_zebra(payload) 
    return response


if __name__ == "__main__":
    options = parse_args()
    response = main(options) 
    print("Printer responded with:", response)
