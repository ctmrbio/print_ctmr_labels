__author__ = "Fredrik Boulund, Marica Hamsten"
__date__ = "2017"
__doc__ = """Print medium label, three lines, according to BARI template."""

import argparse

from field_validators import field_validators

class BARI():
    """BARI label.

    Medium size label, three lines. Example:
    BARI 01
    Feces
    2017.07.07MH
    """

    def initialize_subparser(self, subparsers):
        subparser = subparsers.add_parser("BARI", help="Medium label, three lines.")
    
        subparser.add_argument("--description", "-d", dest="description",
                required=True,
                default="BARI 01",
                type=field_validators.description,
                help="Line 1: Free text, max ca 9 characters.")
        subparser.add_argument("--sample-type", "-s", dest="sample_type",
                required=True,
                default="Feces",
                type=field_validators.sample_type,
                help="Line 2: Free text, max ca 15 characters.")
        subparser.add_argument("--date", "-d", dest="date",
                required=True,
                default="2017.01.01",
                type=field_validators.date,
                help="Line 3: Date (YYYY.MM.DD).")
        subparser.add_argument("--initials", "-i", dest="initials",
                required=True,
                default="MH",
                type=field_validators.initials,
                help="Line 3: Initials, 2 characters.")
        
        subparser.set_defaults(func=BARI)
        return subparser
    
    @staticmethod
    def create_zpl(content):
        """
        Wrap content in ZPL.
        """
        zpl = """^XA
        ^CF0,50
        ^FO40,12^FD{description}^FS
        ^CF0,25
        ^FO40,55^FD{sample_type}^FS
        ^CF0,25
        ^FO40,80^FD{date}{initials}^FS
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
            "description": options.description,
            "sample_type": options.sample_type,
            "date": options.date,
            "initials": options.initials,
            }

        copies = options.copies
        payload = ''.join(self.create_zpl(content) for n in range(0, copies))

        return payload
