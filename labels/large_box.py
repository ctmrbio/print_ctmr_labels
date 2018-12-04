__author__ = "Fredrik Boulund, Marica Hamsten"
__date__ = "2017"
__doc__ = """Print large label, intended for boxes or racks in the freezer."""

import argparse
from functools import partial

from field_validators import field_validators

class LargeBox():
    """Large box label.

    Large label, four lines plus a QR code:
      Project Name
    -----------------
     [QR] CTMR Box 1
     [QR] 2017.06.29
    -----------------
      2017.07.07MH
    """

    def initialize_subparser(self, subparsers):
        subparser = subparsers.add_parser("large_box", help="Medium label, three lines.")
    
        subparser.add_argument("--project", "-p", dest="project",
                required=True,
                default="Project name",
                type=partial(field_validators.free_text, max_length=20),
                help="Line 1: Free text, max ca 20 characters.")
        subparser.add_argument("--description", "-d", dest="description",
                required=True,
                default="CTMR Box 1",
                type=partial(field_validators.free_text, max_length=20), 
                help="Line 2: Free text, max ca 20 characters.")
        subparser.add_argument("--storage-date", "-s", dest="storage_date",
                required=True,
                default="2017.01.01",
                type=field_validators.date,
                help="Line 3: Date (YYYY.MM.DD).")
        subparser.add_argument("--label-date", "-l", dest="label_date",
                required=True,
                default="2017.01.01",
                type=field_validators.date,
                help="Line 4: Date (YYYY.MM.DD).")
        subparser.add_argument("--initials", "-i", dest="initials",
                required=True,
                default="MH",
                type=partial(field_validators.free_text, max_length=4),
                help="Line 4: Initials, max 4 characters.")
        
        subparser.set_defaults(func=LargeBox)
        return subparser
    
    @staticmethod
    def create_zpl(content):
        """
        Wrap content in ZPL.
        """

        centered_project = content["project"].center(20)
        centered_storage_date = content["storage_date"].center(30)
        centered_label_date_initials = "{label_date}{initials}"\
                .format(label_date=content["label_date"], initials=content["initials"])\
                .center(30)

# ^XA                                   ## begin barcode
# ^CF0,50                               ## set font to type 0, height 50
# ^FO50,30^FD{project}^FS               ## set position to 50, 30 && write the project name
# ^FO0,90^GB500,1,3^FS                  ## set position to 0, 90 && draw a horizontal line (box 500x1, thickness 3)
# ^FO50,100                             ## set position to 50, 100
# ^BQN,2,8                              ## begin QR code of "normal, enhanced, zoom=8"
# ^FDQA,{description}^FS                ## print barcode with correction level Q, data input Auto
# ^CF0,50                               ## set font to type 0, height 50
# ^FO250,150^FD{description}^FS         ## set position to 250, 150 && write the description
# ^FO250,220^FD{storage_date}^FS        ## set position to 250, 150 && write the storage date
# ^FO0,300^GB500,1,3^FS                 ## set position to 0, 300 && draw a horizontal line
# ^CF0,20                               ## set font to type 0, height 20
# ^FO40,320^FD{label_date_initials}^FS  ## set position to 40, 320 && write the label date initials
# ^XZ                                   ## end barcode

        zpl = """^XA
        ^CF0,50
        ^FO20,30^FD{project}^FS
        ^FO0,90^GB500,1,3^FS
        ^FO60,100
        ^BQN,2,4
        ^FDQA,{description}^FS
        ^CF0,50
        ^FO170,140^FD{description}^FS
        ^FO0,230^FD{storage_date}^FS
        ^FO0,300^GB500,1,3^FS
        ^CF0,30
        ^FO40,330^FD{label_date_initials}^FS
        ^XZ
        """.format(project=centered_project, 
                description=content["description"],
                storage_date=centered_storage_date, 
                label_date_initials=centered_label_date_initials)
        return zpl

    def make_labels(self, options): 
        """
        Create labels and return a payload for printing.

        The payload may contain multiple copies of the label, according
        to `options.copies`.
        """  

        content = {
            "project": options.project,
            "description": options.description,
            "storage_date": options.storage_date,
            "label_date": options.label_date,
            "initials": options.initials,
            }

        copies = options.copies
        payload = ''.join(self.create_zpl(content) for n in range(0, copies))

        return payload
