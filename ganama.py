#!/usr/bin/env python3

r"""
  ____    _    _   _    _    __  __    _
 / ___|  / \  | \ | |  / \  |  \/  |  / \
| |  _  / _ \ |  \| | / _ \ | |\/| | / _ \
| |_| |/ ___ \| |\  |/ ___ \| |  | |/ ___ \
 \____/_/   \_\_| \_/_/   \_\_|  |_/_/   \_\

      Web Application Fuzzer and Parser
"""

__author__ = "Hüseyin ALTUNKAYNAK"
__copyright__ = "Copyright 2019, Hüseyin ALTUNKAYNAK"
__license__ = "GNU General Public License"
__version__ = "1.0"
__email__ = "huseyin.altunkaynak51@gmail.com"

import sys
import argparse
import gana_fuzzer as gf
import gana_parser as gp

def parser(url_list):
    pass

def fuzzer(url, wordlist):
    pass

if __name__ == "__main__":
    print("GANAMA Project")
    parser = argparse.ArgumentParser(prog="GANAMA",
        description="GANAMA Web Application Fuzzer and Parser",
        epilog="Copyright 2019, huseyince.com")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v" + __version__)
    parser.add_argument("-u", "--url", help="web application url", action="store")
    parser.add_argument("-w", "--wordlist", help="custom wordlist", action="store")
    parser.add_argument("-o", "--output", help="store source codes and reports location", action="store")
    args = parser.parse_args()

    if not args.url:
        print("usage: python3 ganama.py -h")
    if args.url:
        if args.url.split(":")[0] not in ["http", "https"]:
            print("Checkout your URL http:// or https://")
            sys.exit(0)

    if not args.output:
        args.output = "gana_out_" + args.url.split("://")[1]
    
    if not args.wordlist:
        args.wordlist = "common.txt"
    
    clean_list, garbage_list = gp.main(args.url)

    for url in clean_list:
        print(url)
