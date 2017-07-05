__author__ = "Fredrik Boulund, Hugo Wefer"
__date__ = "2017"
__doc__ = """Print small barcode labels, intended for sample collection tubes."""

import argparse

from field_validators import field_validators

class ProjectBarcodes():
    """Project barcode labels.

    Small label, one EAN13 barcode.
    """

    def initialize_subparser(self, subparsers):
        subparser = subparsers.add_parser("project_barcodes", help="Small label, one EAN13 barcode.")

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
                default="Project ID",
                type=field_validators.project_id,
                help="A valid three digit project ID.")
        
        subparser.set_defaults(func=ProjectBarcodes)
        return subparser
    
    @staticmethod
    def create_zpl(content):
        """
        Wrap content in ZPL.
        """

        zpl = """^XA^LL150
        ^FO30,20^BY1.5
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
                        "project_id": options.project,
                        "sample_id": sample_id,
                        }

                copies = options.copies
                payload.append(''.join(self.create_zpl(content) for n in range(0, copies)))
                
        return ''.join(payload)
