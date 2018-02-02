__author__ = "Fredrik Boulund, Kim Wong"
__date__ = "2018"
__doc__ = """Print small barcode labels, intended for sample collection tubes. For Ulrika Zagai's projects."""

import argparse

from field_validators import field_validators

class ZagaiBarcodes():
    """Project barcode labels for Ulrika Zagai's projects.

    Small label, one EAN13 barcode.
    A two digit project ID is required as input, and given the prefix 7 for identification as a
    Zagai project. e.g. '23' is input and the resultant ID becomes '723'.
    """

    def initialize_subparser(self, subparsers):
        subparser = subparsers.add_parser("zagai_barcodes", help="Small label, one EAN13 barcode.")

        subparser.add_argument("--start", "-s", dest="start",
                required=True,
                default=0,
                type=int, 
                help="Starting sample ID.")
        subparser.add_argument("--end", "-e", dest="end",
                required=True,
                default=0,
                type=int, 
                help="Ending sample ID.")
        subparser.add_argument("--project", "-p", dest="project",
                required=True,
                default="Zagai Project ID",
                type=field_validators.zagai_project_id,
                help="A valid two digit project ID.")
        
        subparser.set_defaults(func=ZagaiBarcodes)
        return subparser
    
    @staticmethod
    def create_zpl(content):
        """
        Wrap content in ZPL.
        """

        zpl = """^XA^LL150
        ^FO50,20^BY1.5
        ^BEN,50,Y,N
        ^FD{project_id}{sample_id:09d}^FS
        ^XZ
        """.format(**content)

        return zpl

    def make_labels(self, options):
        """
        Create labels and return a payload for printing.

        The payload may contain multiple copies of each barcode, 
        according to `options.copies`.
        """

        payload = []
        for sample_id in range(options.start, options.end+1):
                content = {
                        "project_id": '7' + options.project,
                        "sample_id": sample_id,
                        }

                copies = options.copies
                payload.append(''.join(self.create_zpl(content) for n in range(0, copies)))
                
        return ''.join(payload)
