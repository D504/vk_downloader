__author__ = 'zabidon'

import argparse

def arg_parse():
    argparser = argparse.ArgumentParser()

    argparser.add_argument("-i", "--id",
                            type=int,
                            help="User ID",
                            metavar="USER_ID",
                            dest="id",
                            required=False)
    argparser.add_argument("-a", "--aid",
                            type=int,
                            help="Album ID",
                            metavar="-ALBUM_ID",
                            dest="aid",
                            required=False)
    argparser.add_argument("-t", '--through_albums',
                           action='store_true',
                           help="All audios download to albums subdirectory",
                           required=False)

    args = argparser.parse_args()
    return args