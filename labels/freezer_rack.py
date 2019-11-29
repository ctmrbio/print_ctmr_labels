__author__ = "Fredrik Boulund, Alexandra Pennhag"
__date__ = "2019"
__doc__ = """Print freezer rack label."""

import argparse
from functools import partial

from field_validators import field_validators

class FreezerRack():
    """Large label.

    Large label, four lines plus a QR code:
      Project Name
    -----------------
      FIELD1
    -----------------
      FIELD2
    """

    def initialize_subparser(self, subparsers):
        subparser = subparsers.add_parser("freezer_rack", help="Medium label, three lines.")
    
        subparser.add_argument("--project", "-p", dest="project",
                required=True,
                default="Project name",
                type=partial(field_validators.free_text, max_length=20),
                help="Line 1: Free text, max ca 20 characters.")
        subparser.add_argument("--field1", "-d", dest="field1",
                required=False,
                default="",
                type=partial(field_validators.free_text, max_length=20), 
                help="Line 2: Free text, max ca 20 characters.")
        subparser.add_argument("--field2", "-D", dest="field2",
                required=False,
                default="CTMR",
                type=partial(field_validators.free_text, max_length=20),
                help="Line 3: [max 20 chars].")
        
        subparser.set_defaults(func=FreezerRack)
        return subparser
    
    @staticmethod
    def create_zpl(content):
        """
        Wrap content in ZPL.
        """

        centered_project = content["project"].center(20)

# ^XA                                   ## begin barcode
# ^CF0,50                               ## set font to type 0, height 50
# ^FO50,30^FD{project}^FS               ## set position to 50, 30 && write the project name
# ^FO0,90^GB500,1,3^FS                  ## set position to 0, 90 && draw a horizontal line (box 500x1, thickness 3)
# ^CF0,50                               ## set font to type 0, height 50
# ^FO20,150^FD{field1}^FS              ## set position to 250, 150 && write the description
# ^FO0,300^GB500,1,3^FS                 ## set position to 0, 300 && draw a horizontal line
# ^CF0,20                               ## set font to type 0, height 20
# ^FO20,320^FD{field2}^FS               ## set position to 40, 320 && write the label date initials
# ^XZ                                   ## end barcode

        zpl = """^XA
        ^CF0,50
        ^FO20,30^FD{project}^FS
        ^FO0,90^GB500,1,3^FS
        ^CF0,50
        ^FO55,140^FD{field1}^FS
        ^FO0,300^GB500,1,3^FS
        ^CF0,30
        ^FO55,330^FD{field2}^FS
        ^XZ
        """.format(project=centered_project, 
                field1=content["field1"],
                field2=content["field2"])
        return zpl

    def make_labels(self, options): 
        """
        Create labels and return a payload for printing.

        The payload may contain multiple copies of the label, according
        to `options.copies`.
        """  

        content = {
            "project": options.project,
            "field1": options.field1,
            "field2": options.field2,
            }

        copies = options.copies
        payload = ''.join(self.create_zpl(content) for n in range(0, copies))

        return payload
