__author__ = "Fredrik Boulund, Kim Wong"
__date__ = "2018"
__doc__ = """Field validators for Zebra labels."""

import argparse

class field_validators():
    """
    Field validators for BARI labels.
    """

    @staticmethod
    def free_text(text, max_length=15):
        if len(text) > max_length:
            msg = "Field must be less than {} characters.".format(max_length)
            raise argparse.ArgumentTypeError(msg)
        else:
            return text

    @staticmethod
    def description(desc, max_length=9):
        if len(desc) > max_length:
            msg = "Description must be less than {} characters.".format(max_length)
            raise argparse.ArgumentTypeError(msg)
        else:
            return desc

    @staticmethod
    def sample_type(sample_type, max_length=15):
        if len(sample_type) > max_length:
            msg = "Sample type must be less than {} characters.".format(max_length)
            raise argparse.ArgumentTypeError(msg)
        else:
            return sample_type

    @staticmethod
    def date(date):
        dsplit = date.split(".")
        if len(dsplit) != 3 or len(dsplit[0]) != 4 or len(dsplit[1]) != 2 or len(dsplit[2]) != 2:
            msg = "Date must be in YYYY.MM.DD format."
            raise argparse.ArgumentTypeError(msg)
        else:
            return date

    @staticmethod
    def initials(initials, chars=2):
        if len(initials) != chars:
            msg = "Initals must consist of exactly {} letters.".format(chars)
            raise argparse.ArgumentTypeError(msg)
        else:
            return initials.upper()

    @staticmethod
    def project_id(pid):
        if len(pid) != 3:
            msg = "Project ID must consist of exactly three digits."
            raise argparse.ArgumentTypeError(msg)
        elif pid[0] == 7:
            msg = "Project ID may not begin with a 7."
            raise argparse.ArgumentTypeError(msg)
        else:
            return pid

    @staticmethod
    def zagai_project_id(pid):
        if len(pid) != 2:
            msg = "Project ID must consist of exactly two digits."
            raise argparse.ArgumentTypeError(msg)
        else:
            return pid

    @staticmethod
    def exact_length(string, length=4):
        if len(string) != length:
            msg = "Project ID must consist of exactly {length} digits.".format(length=length)
            raise argparse.ArgumentTypeError(msg)
        else:
            return string
