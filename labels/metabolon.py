__author__ = "Fredrik Boulund, Marica Hamsten"
__date__ = "2018"
__doc__ = """Print medium label, three lines, according to Metabolon template."""

import os
import argparse
from functools import partial

from .field_validators import field_validators

class Metabolon():
    """Metabolon template

    Medium size label, three lines. Example:
    <sample_id>
    250 ul
    2018.07.02 MA
    """

    def initialize_subparser(self, subparsers):
        subparser = subparsers.add_parser("metabolon", help="Medium label, three lines.")
    
        subparser.add_argument("--title", "-t", dest="title",
                required=True,
                default="",
                help="Line 1: Parsed line by line from a text file (NO EXCEL FILES!).")
        subparser.add_argument("--headers", dest="headers",
                default=False,
                action="store_true",
                help="The input file has a header line.")
        subparser.add_argument("--description", "-d", dest="description",
                required=True,
                default="250 ul",
                type=partial(field_validators.free_text, max_length=20), 
                help="Line 2: Free text, max ca 15 characters.")
        subparser.add_argument("--date", "-D", dest="date",
                required=True,
                default="2018.01.01",
                type=field_validators.date,
                help="Line 3: Date (YYYY.MM.DD).")
        subparser.add_argument("--initials", "-i", dest="initials",
                required=True,
                default="MH",
                type=field_validators.initials,
                help="Line 3: Initials, 2 characters.")
        
        subparser.set_defaults(func=Metabolon)
        return subparser
    
    @staticmethod
    def create_zpl(content):
        """
        Wrap content in ZPL.
        """
        zpl = """^XA
        ^CF0,30
        ^FO50,10^FD{title}^FS
        ^CF0,20
        ^FO50,43^FD{description}^FS
        ^CF0,20
        ^FO50,70^FD{date} {initials}^FS
        ^XZ
        """.format(**content)
        return zpl

    def parse_sample_list(self, options):
        sample_ids = [line.strip().split()[0] for line in open(options.title)]
        if options.headers:
            self.sample_ids = sample_ids[1:]
        else:
            self.sample_ids = sample_ids


    def make_labels(self, options): 
        """
        Create labels and return a payload for printing.

        The payload may contain multiple copies of the label, according
        to `options.copies`.
        """  

        self.parse_sample_list(options)

        super_payload = []
        for sample_id in self.sample_ids:
            content = {
                "title": sample_id,
                "description": options.description,
                "date": options.date,
                "initials": options.initials,
                }

            copies = options.copies
            payload = ''.join(self.create_zpl(content) for n in range(0, copies))
            super_payload.append(payload)
            
        return ''.join(super_payload)
