#!/usr/bin/env python

import sys
import os
from argparse import ArgumentParser
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from standings import Standings


def load_config(file='~/.evestandings.conf'):
    config = ConfigParser()
    file = os.path.expandvars(os.path.expanduser(file))
    if os.path.exists(file):
        config.read(file)
        outconfig = object()
        for name, val in config.items('standings'):
            setattr(outconfig, name, val)
        return outconfig
    else:
        return object()


def main():
    parser = ArgumentParser(prog='EVEStandings', description='Outputs a EVE corporation/alliance standings to a HTML page')
    parser.add_argument('-k', '--keyid', help='Key ID of the API key')
    parser.add_argument('-v', '--vcode', help='vCode of the API key')
    parser.add_argument('-C', '--config', help='Path to your configuration file')
    parser.add_argument('-f', '--output', help='Output the resulting HTML to a file')
    parser.add_argument('--template', help='Location of a customized template to use instead of the default')

    ns = parser.parse_args()

    if ns.keyid and ns.vcode:
        conf = ns
    else:
        if ns.config:
            conf = load_config(ns.config)
        else:
            conf = load_config()
    if not hasattr(conf, 'keyid') or not hasattr(conf, 'vcode') or not conf.keyid or not conf.vcode:
        sys.stderr.write('Key ID or vCode is missing, please provide both on the command line or in the config file\n')
        parser.print_help()
        sys.exit(1)

    obj = Standings(conf.keyid, conf.vcode)
    if ns.template:
        output = obj.render_template(ns.template)
    else:
        output = obj.html()

    if conf.output:
        f = open(os.path.expanduser(conf.output), 'w')
        f.write(output)
        f.close()
    else:
        sys.stdout.write(output)

    sys.exit(0)


if __name__ == '__main__':
    main()