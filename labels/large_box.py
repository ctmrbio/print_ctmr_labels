__author__ = "Fredrik Boulund, Marica Hamsten"
__date__ = "2017"
__doc__ = """Print large label, intended for boxes or racks in the freezer."""

import argparse
from functools import partial

from field_validators import field_validators

class LargeBox():
    """Large box label.

    Large label, four lines:
    Project Name
    ------------
     CTMR Box 1
     2017.06.29
    ------------
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
                type=partial(field_validators.initials, chars=4),
                help="Line 4: Initials, max 4 characters.")
        
        subparser.set_defaults(func=LargeBox)
        return subparser
    
    @staticmethod
    def create_zpl(content):
        """
        Wrap content in ZPL.
        """

        centered_project = content.project.center(20)
        centered_storage_date = content.storage_date.center(30)
        centered_label_date_initials = "{storage_date}{initials}"\
                .format(content.label_date, content.initials)\
                .center(30)

        zpl = """^XA
        ^CF0,80 ^FO40,30^FD{project}^FS
        ^FO0,120^GB500,1,3^FS
        ^CF0,50 
        ^FO40,50^FD{description}^FS
        ^FO40,50^FD{storage_date}^FS
        ^FO0,300^GB500,1,3^FS
        ^CF0,20 ^FO40,80^FD{label_date_initials}^FS
        ^XZ
        """.format(centered_project, 
                content.description, 
                centered_storage_date, 
                centered_label_date_initials)
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
