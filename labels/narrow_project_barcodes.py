__author__ = "Fredrik Boulund, Hugo Wefer"
__date__ = "2017"
__doc__ = """Print small barcode labels, intended for sample collection tubes."""

import argparse
from itertools import zip_longest

from .field_validators import field_validators


class NarrowProjectBarcodes():
    """Narrow project barcode labels.

    Tiny label, one EAN13 barcode.
    """

    def initialize_subparser(self, subparsers):
        subparser = subparsers.add_parser("narrow_project_barcodes", help="Tiny label, one EAN13 barcode.")

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
        
        subparser.set_defaults(func=NarrowProjectBarcodes)
        return subparser
    
    @staticmethod
    def create_zpl(content_1, content_2):
        """
        Wrap pairs of content in ZPL.
        """

        zpl_1 = """
        ^XA
        ^LL250
        ^FO100,02
        ^BY1.5
        ^BEN,20,Y,N
        ^FD{project_id}{sample_id:09d}^FS
        """.format(**content_1)

        if content_2 is None:
            zpl_2 = "^XZ"
        else:
            zpl_2 = """
            ^FO500,02
            ^BY1.5
            ^BEN,20,Y,N
            ^FD{project_id}{sample_id:09d}^FS
            ^XZ
            """.format(**content_2)

        return zpl_1 + zpl_2

    @staticmethod
    def _grouper(iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        print(iterable)
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    def make_labels(self, options):
        """
        Create labels and return a payload for printing.

        The payload may contain multiple copies of each barcode, 
        according to `options.copies`.
        """

        payload = []
        contents = []
        for sample_id in range(options.start, options.end+1):
                for copy_number in range(options.copies):
                        contents.append({
                                "project_id": options.project,
                                "sample_id": sample_id,
                                }
                        )
        
        for content_1, content_2 in self._grouper(contents, 2):
                payload.append(''.join(self.create_zpl(content_1, content_2)))

                
        return ''.join(payload)
