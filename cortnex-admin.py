#!/usr/bin/env python3

"""
MIT License
Copyright (c) 2021 Ygor Simões
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
from threading import Thread
from time import sleep

from src.core.config import Config
from src.core.color import Color
from src.core.banner import Strings
from src.core.update import Update

from src.request.user_agent import UserAgent
from src.request.proxy import Proxy
from src.request.request import Request

from src.finder import Finder
from src.utils.wordlist import Wordlist

# Try to import libraries.
try:
    from requests import get
except ModuleNotFoundError as ex:
    Color.println("{!} %s Please install requirements: {R}pip3 install -r requirements.txt{W}" % ex)

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument("-h", "--help",
                    action="store_true",
                    help="Show this help message and exit")

parser.add_argument("-u", "--url",
                    action="store",
                    type=str,
                    default=False,
                    help="Target URL (https://www.site_target.com/)")

parser.add_argument("-t", "--threads",
                    action="store",
                    type=int,
                    default="8",
                    help="Set threads number. Default: 8")

parser.add_argument("-w", "--wordlist",
                    action="store",
                    type=str,
                    default="1",
                    help="Set wordlist. Default: 1 (Small) and Max: 3 (Big)")

parser.add_argument("-p", "--proxy",
                    action="store",
                    type=str,
                    default=None,
                    help="Use a proxy to connect to the target URL")

parser.add_argument("--random-proxy",
                    action="store_true",
                    default=False,
                    help="Use a random anonymous proxy")

parser.add_argument("--user-agent",
                    action="store",
                    type=str,
                    default=None,
                    help="Customize the User-Agent. Default: Random User-Agent")

parser.add_argument("--no-redirects",
                    action="store_false",
                    help="Disables that redirects should be followed.")

parser.add_argument("--update",
                    action="store_true",
                    default=False,
                    help="Upgrade CORTNEX to its latest available version")

parser.add_argument("--no-update",
                    action="store_true",
                    default=False,
                    help="Disables the intention of updates")

parser.add_argument("--no-logo",
                    action="store_true",
                    default=False,
                    help="Disable the initial banner")

if __name__ == '__main__':

    # Stores all command line arguments passed in the variable.
    args = parser.parse_args()

    # Get the CORTNEX settings, updates and pass it on to the Strings class.
    String = Strings()

    # Print the banner along with CORTNEX specifications.
    if not args.no_logo:
        String.banner()
        String.banner_description()

    # Check for available updates.
    update = Update()

    if args.update and update.verify(args.update):
        update.upgrade()

    if Config.get_automatic_verify_upgrades and not args.update:
        update.verify(args.update)

    # Activates the "helper()" method if no targets are passed in the arguments.
    if not args.url:
        String.helper()
        exit()
    else:
        # Format the target URL accordingly.
        args.url = Config.target(args.url)

        # Instance the "Request" class.
        user_agent = UserAgent(args)
        # Generates a random User-Agent.
        args.user_agent = user_agent.run()

        # Formats the selected proxy.
        proxy = Proxy(args)

        if args.proxy is not None:
            args.proxy = proxy.format_proxy()
        else:
            if args.random_proxy:
                args.proxy = proxy.random_proxy()

        # Instance the "Check" class.
        request = Request(args)

        # Checks whether the target is online.
        if request.check_status() == 200:
            Color.println("{+} Target On: {G}%s{W}" % args.url)
        else:
            Color.println("{!} Error: Please verify your target.")
            exit()

        # Stores the selected word list in the variable.
        wordlist = Wordlist(args)
        args.wordlist = wordlist.run()

        ExploitFinder = Finder(args)  # Instance the "Finder" class.

        # CORTNEX, find!
        ExploitFinder.dashboard()

        Color.println("\n{+} {G}CORTNEX, find the dashboard!{W}\n")
        ExploitFinder.run()
