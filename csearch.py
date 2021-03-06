#!/usr/bin/env python3
import os, re
import subprocess as sub
import argparse


# Bash colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
NC  = '\033[0m'


def _clean(string):
    '''
    prepares string for insertion into _cat_search regex.
    '''
    escape_chars = ".^$*+?{}[]|()"
    replace_chars = ['\.', '\^', '\$', '\*', '\+', '\?',
        '\{', '\}', '\[', '\]', '\|', '\(', '\)'] 
    out = string
    for og, replace in zip(escape_chars, replace_chars):
        out = out.replace(og, replace)
    return(out)


def _search(fname, token, search_string, display_func):
    try:
        out = sub.check_output(search_string, shell=1)
        out = out.decode('utf-8')
        display_func(out)
    except sub.CalledProcessError:
        # grep errors if it doesn't find anything
        pass


def _nm_search(fname, token):

    def nm_display_func(string):
        split  = string.split()
        for word in split:
            if token in word:
                print("{}{}{}: {}".format(RED, fname, NC, line))
        
    search_string = 'nm -D -C {} 2> /dev/null | grep -n \"{}\"'.format(fname, token)
    _search(fname, token, search_string, nm_display_func)


def _cat_search(fname, token):
    cat_re = re.compile(r"""
        ^(?P<line_no>(\d*)):
        (?P<stuff1>(.*))
        (?P<token>({}))
        (?P<stuff2>(.*))
        """.format(_clean(token)),
        re.VERBOSE)

    def cat_display_func(string):
        lines = string.split('\n')
        for line in lines:
            m = cat_re.search(line)
            if m:
                line_no = m.group('line_no')
                stuff1 = m.group('stuff1')
                stuff2 = m.group('stuff2')
                print("{}{}{}: {}{}{}: {}{}{}{}{}".format(RED, fname, NC, 
                    GREEN, line_no, NC, stuff1, RED, token, NC, stuff2))

    search_string = 'cat {} | grep -n \"{}\"'.format(fname, token)
    _search(fname, token, search_string, cat_display_func)


def _check_regex(string, regex):
    m = regex.search(string)
    if m:
        return(True)
    return(False)


def _is_c_header(fname):
    r = re.compile(r'\.(?P<extension>((h)|(hpp)))$')
    return(_check_regex(fname, r))


def _is_c_source(fname):
    r = re.compile(r'\.(?P<extension>((c)|(cu)|(cpp)))$')
    return(_check_regex(fname, r))


def _is_object_file(fname):
    r = re.compile(r'\.(?P<extension>((so)|(a)|(o)))(\.|$)')
    return(_check_regex(fname, r))


def _search_directory(dname, token, type_check_fun, search_fun, r):
    contents = os.listdir(dname)
    for thing in contents:
        thing = os.path.join(dname, thing)
        if os.path.isfile(thing):
            if type_check_fun(thing):
                search_fun(thing, token)
        elif (r and os.path.isdir(thing)):
            _search_directory(thing, token, type_check_fun, search_fun, r)


def search_main(name, token, type_check_fun, search_fun, r):
    if os.path.isfile(name):
        if type_check_fun(name):
            search_fun(name, token)
        else:
            raise TypeError("Incorrect file type.")
    elif os.path.isdir(name):
        _search_directory(name, token, type_check_fun, search_fun, r)
    else:
        raise TypeError("Must be a directory or file.")


def object_main(name, token, r):
    search_main(name, token, _is_object_file, _nm_search, r)


def source_main(name, token, r):
    search_main(name, token, _is_c_source, _cat_search, r)


def header_main(name, token, r):
    search_main(name, token, _is_c_header, _cat_search, r)


def main():
    descr = '''
    Utility for locating symbols in C/C++ object files (on Linux).
    '''

    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=descr)
    parser.add_argument('--recursive', '-r', '-R',
        action='store_true',
        default=False,
        help="Recursive mode. Causes subdirectories to be searched.")
    parser.add_argument('--object', '-o',
        action='store_true',
        default=False,
        help='Object mode. Searches object files for a symbol.')
    parser.add_argument('--source', '-s',
        action='store_true',
        default=False,
        help='Source mode. Searches C/C++/Cuda source files for a symbol.')
    parser.add_argument('--header', '-he',
        action='store_true',
        default=False,
        help='Header mode. Searches C/C++/Cuda header files for a symbol.')
    parser.add_argument('--target', '-t',
        action='store',
        type=str,
        default='.',
        help='Directory or file to search.')
    parser.add_argument('symbol',
        metavar='symbol',
        type=str,
        nargs='+',
        help='symbol to find')
    args = parser.parse_args()
    target = os.path.abspath(args.target)
    symbol = args.symbol[0]
    o_mode = args.object
    s_mode = args.source
    h_mode = args.header
    r = args.recursive
    if not (o_mode or s_mode or h_mode):
        raise Exception("Must select a mode of operation (-s or -o)")

    if o_mode:
        object_main(target, symbol, r)
    if s_mode:
        source_main(target, symbol, r)
    if h_mode:
        header_main(target, symbol, r)


if __name__ == '__main__':
    main()
