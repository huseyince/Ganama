#!/usr/bin/env python3

__author__ = "Hüseyin ALTUNKAYNAK"
__copyright__ = "Copyright 2019, Hüseyin ALTUNKAYNAK"
__license__ = "GNU General Public License"
__version__ = "1.0"
__email__ = "huseyin.altunkaynak51@gmail.com"

import sys, os
import argparse
import shutil
from urllib.parse import urlsplit
import gana_fuzzer as gf
import gana_parser as gp


NOCOLOR='\033[0m'
WHITE='\033[1;37m'
RED='\033[1;31m'
ORANGE='\033[0;33m'
BLUE='\033[1;34m'
YELLOW='\033[1;33m'
GREEN='\033[1;32m'
PURPLE='\033[1;35m'
CYAN='\033[1;36m'

banner = WHITE + r"""
  ____    _    _   _    _    __  __    _
 / ___|  / \  | \ | |  / \  |  \/  |  / \
| |  _  / _ \ |  \| | / _ \ | |\/| | / _ \
| |_| |/ ___ \| |\  |/ ___ \| |  | |/ ___ \
 \____/_/   \_\_| \_/_/   \_\_|  |_/_/   \_\

     Web Application Parser and Fuzzer
""" + NOCOLOR

web_file_extension = [
    "asp",
    "aspx",
    "axd",
    "asx",
    "asmx",
    "ashx",
    "cfm",
    "yaws",
    "swf",
    "html",
    "htm",
    "xhtml",
    "jhtml",
    "jsp",
    "jspx",
    "wss",
    "do",
    "action",
    "pl",
    "php",
    "php4",
    "php3",
    "phtml",
    "py",
    "rb",
    "rhtml",
    "shtml",
    "svg",
    "cgi",
    "dll",
]

def main_parser(base_url: str) -> list:
    file_list = []
    clean_list, garbage_list = gp.main(base_url)

    for url in clean_list:
        print(YELLOW + "[+] " + url)
        if "." in urlsplit(url).path and urlsplit(url).path.split(".")[-1] not in web_file_extension:
            file_list.append(url)
            continue

        try:
            sub_clean_list, sub_garbage_list = gp.main(url)
        except Exception as err:
            print(err)
            output("last_error", clean_list, file_list, garbage_list)

        for clea in sub_clean_list:
            if clea not in clean_list:
                clean_list.append(clea)

        for garb in sub_garbage_list:
            if garb not in garbage_list:
                garbage_list.append(garb)

    for url in file_list:
        clean_list.remove(url)

    return [clean_list, garbage_list, file_list]

def main_fuzzer(url, wordlist):
    pass

def report2file(path: str, clean_list: list, garbage_list: list, file_list: list):
    with open(path + "/clean.txt", "w") as f:
        for url in clean_list:
            f.write("%s\n" % url)
    
    with open(path + "/garbage.txt", "w") as f:
        for url in garbage_list:
            f.write("%s\n" % url)

    with open(path + "/file.txt", "w") as f:
        for url in file_list:
            f.write("%s\n" % url)

def output(output_name: str, clean_list: list, garbage_list: list, file_list: list):
    path = "Reports/" + output_name

    try:
        os.mkdir(path)
    except FileExistsError:
        for r_file in os.listdir(path):
            os.remove(path + "/" + r_file)
        report2file(path, clean_list, garbage_list, file_list)
        print(GREEN + "\n[+] Report saved successfully in " + path)
    except OSError:
        print(RED + "\n[!] Directory not created!")
        path = "/tmp/Ganama/" + path
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass

        try:
            os.mkdir("/tmp/Ganama")
        except FileExistsError:
            pass

        try:
            os.mkdir(path)
        except OSError:
            print(RED + "\n[!] Oops! " + path + " not created.")
            print(BLUE + "\n[-->] CLEAN LIST")
            for url in clean_list:
                print(ORANGE + "[+] " + url)
            print(BLUE + "\n[-->] FILE LIST")
            for url in file_list:
                print(ORANGE + "[+] " + url)
            print(BLUE + "\n[-->] GARBAGE LIST")
            for url in garbage_list:
                print(ORANGE + "[+] " + url)
        else:
            report2file(path, clean_list, garbage_list, file_list)
            print(GREEN + "\n[+] Report saved in /tmp/Ganama/" + path)
    else:
        report2file(path, clean_list, garbage_list, file_list)
        print(GREEN + "\n[+] Report successfully saved in " + path)

if __name__ == "__main__":
    print(banner)
    parser = argparse.ArgumentParser(prog="GANAMA",
        description="GANAMA Web Application Fuzzer and Parser",
        epilog="Copyright 2019, huseyince.com")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v" + __version__)
    parser.add_argument("-u", "--url", help="web application url", action="store")
    parser.add_argument("-w", "--wordlist", help="custom wordlist", action="store")
    parser.add_argument("-o", "--output", help="store source codes and reports location", action="store")
    args = parser.parse_args()

    if not args.url:
        print(RED + "usage: python3 ganama.py -h")
        sys.exit(0)
    if args.url:
        if args.url.split(":")[0] not in ["http", "https"]:
            print(RED + "Checkout your URL http:// or https://")
            sys.exit(0)

    if args.output:
        args.output = args.output
    else:
        args.output = args.url.split("://")[1].split("/")[0]
    
    if not args.wordlist:
        args.wordlist = "common.txt"
    
    lists = main_parser(args.url)

    output(args.output, lists[0], lists[1], lists[2])