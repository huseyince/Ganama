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

import argparse
import gana_fuzzer as gf
import gana_parser as gp



if __name__ == "__main__":
    base_url = "https://huseyince.com"

    parser = argparse.ArgumentParser(prog="GANAMA",
        description="GANAMA Web Application Fuzzer and Parser",
        epilog="Copyright 2019, huseyince.com")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v" + __version__)
    parser.add_argument("-p", "--parser", help="parse application", action="store_true")
    parser.add_argument("-f", "--fuzzer", help="fuzz application", action="store_true")
    parser.add_argument("-o", "--output", help="store source codes and reports location", action="store_true")
    args = parser.parse_args()

    if args.parser:
        pass

    if args.fuzzer:
        pass

    if args.output:
        pass