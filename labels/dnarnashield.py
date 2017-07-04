__author__ = "Fredrik Boulund, Marica Hamsten"
__date__ = "2017"
__doc__ = """Print medium label, three lines, according to DNA/RNA shield template."""

import argparse
from functools import partial

from field_validators import field_validators

class DnaRnaShield():
    """DNA/RNA shield label.

    Medium size label, three lines. Example:
    DNA/RNA Shield
    R1100-250, ZRC123456
    2017.07.07MH
    """

    def initialize_subparser(self, subparsers):
        subparser = subparsers.add_parser("DnaRnaShield", help="Medium label, three lines.")
    
        subparser.add_argument("--title", "-t", dest="title",
                required=True,
                default="DNA/RNA Shield",
                type=field_validators.free_text,
                help="Line 1: Free text, max ca 15 characters.")
        subparser.add_argument("--description", "-d", dest="description",
                required=True,
                default="R1100-250, ZRC123456",
                type=field_validators.free_text, 
                help="Line 2: Free text, max ca 15 characters.")
        subparser.add_argument("--date", "-D", dest="date",
                required=True,
                default="2017.01.01",
                type=field_validators.date,
                help="Line 3: Date (YYYY.MM.DD).")
        subparser.add_argument("--initials", "-i", dest="initials",
                required=True,
                default="MH",
                type=field_validators.initials,
                help="Line 3: Initials, 2 characters.")
        
        subparser.set_defaults(func=DnaRnaShield)
        return subparser
    
    @staticmethod
    def create_zpl(content):
        """
        Wrap content in ZPL.
        """
        zpl = """^XA
        ^CF0,40
        ^FO10,10^FD{title}^FS
        ^CF0,25
        ^FO10,50^FD{description}^FS
        ^CF0,25
        ^FO10,80^FD{date}{initials}^FS
        ^XZ
        """.format(**content)
        return zpl

    def make_labels(self, options): 
        """
        Create labels and return a payload for printing.

        The payload may contain multiple copies of the label, according
        to `options.copies`.
        """  

        content = {
            "title": options.title,
            "description": options.description,
            "date": options.date,
            "initials": options.initials,
            }

        copies = options.copies
        payload = ''.join(self.create_zpl(content) for n in range(0, copies))

        return payload
