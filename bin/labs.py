#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tretas.org maintenance scripts
'''

# Imports

import getopt
import sys
import os.path

sys.path.append(os.path.abspath('../lib/'))
sys.path.append(os.path.abspath('../labs_django/'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'labs_django.settings'

import django
django.setup()

def usage():
    print '''Usage: %(script_name)s [options]\n
    Commands:
        --read_change       Read the exchange rates from BdP

        -h
        --help              This help screen

    ''' % { 'script_name': sys.argv[0] }


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                    'hv',
                                   ['help',
                                    'read_change',
                                    'verbose',
                                   ])
    except getopt.GetoptError, err:
        print str(err)
        print
        usage()
        sys.exit(1)

    # Defaults
    verbose = False

    # Options
    for o, a in opts:
        if o in ('-v', '--verbose'):
            verbose = True

    # Commands
    for o, a in opts:
        if o == '--read_change':
            from exchange_reader import ExchangeReader

            reader = ExchangeReader()
            reader.run()

            sys.exit()

    # Show the help screen if no commands given
    usage()
    sys.exit()
