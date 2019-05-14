__author__ = "Fredrik Boulund"
__date__ = "2019"
__doc__ = """Print small barcode labels, intended for sample collection tubes."""

import argparse

from field_validators import field_validators

class RomansBarcodes():
    """Project barcode labels.

    Small label, one Code 128 barcode.
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
                default="114",
                type=field_validators.project_id,
                help="A valid three digit project ID.")
        subparser.add_argument("--sample-type", dest="sample_type",
                required=True,
                default="fece",
                type=field_validators.exact_length,
                help="Four letter sample type.")

        subparser.set_defaults(func=ProjectBarcodes)
        return subparser

    @staticmethod
    def create_zpl(content):
        """
        Wrap content in ZPL.
        """

        zpl = """^XA^LL150
        ^FO50,20^BY1.5
        ^BCN,50,Y,N,Y,D
        ^FD{project_id}{sample_type}{sample_id:05d}^FS
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
                        "sample_type": options.sample_type,
                        "sample_id": sample_id,
                        }

                copies = options.copies
                payload.append(''.join(self.create_zpl(content) for n in range(0, copies)))

        return ''.join(payload)
