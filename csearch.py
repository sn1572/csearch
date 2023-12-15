#!/usr/bin/env python3
import os, re
import subprocess as sub
import argparse


# Bash colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
NC  = '\033[0m'


def clean(string):
    '''
    prepares string for insertion into catsearch regex.
    '''
    escape_chars = ".^$*+?{}[]|()"
    replace_chars = ['.', '^', '$', '*', '+', '?',
        '{', '}', '[', ']', '|', '(', ')'] 
    out = string
    for og, replace in zip(escape_chars, replace_chars):
        out = out.replace(og, replace)
    return(out)


def search(fname, token, search_string, display_func):
    try:
        out = sub.check_output(search_string, shell=1)
        out = out.decode('utf-8')
        display_func(out)
    except sub.CalledProcessError:
        # grep errors if it doesn't find anything
        pass


def nm_display_func(fname, token, string):
    split  = string.split('\n')
    for word in split:
        if token in word:
            print("{}{}{}: {}".format(RED, fname, NC, word))


def nmsearch(fname, token):
    display_func = lambda string: nm_display_func(fname, token, string)
    for flag in ("-D", ""):
        search_string = (f"nm {flag} --defined-only -C -l {fname} 2> "
                         f"/dev/null | grep -n \"{token}\"")
        search(fname, token, search_string, display_func)


def cat_display_func(fname, token, string, cat_re):
    lines = string.split('\n')
    for line in lines:
        m = cat_re.search(line)
        if m:
            line_no = m.group('line_no')
            stuff1 = m.group('stuff1')
            stuff2 = m.group('stuff2')
            print("{}{}{}: {}{}{}: {}{}{}{}{}".format(RED, fname, NC, 
                  GREEN, line_no, NC, stuff1, RED, token, NC, stuff2))


def catsearch(fname, token):
    cat_re = re.compile(r"""
        ^(?P<line_no>(\d*)):
        (?P<stuff1>(.*))
        (?P<token>({}))
        (?P<stuff2>(.*))
        """.format(clean(token)),
        re.VERBOSE)
    display_func = lambda string: cat_display_func(fname, token, string,
                                                   cat_re)
    search_string = 'cat {} | grep -n \"{}\"'.format(fname, token)
    search(fname, token, search_string, display_func)


def check_regex(string, regex):
    m = regex.search(string)
    if m:
        return(True)
    return(False)


def is_c_header(fname):
    r = re.compile(r'\.(?P<extension>((h)|(hpp)))$')
    return(check_regex(fname, r))


def is_c_source(fname):
    r = re.compile(r'\.(?P<extension>((c)|(cu)|(cpp)))$')
    return(check_regex(fname, r))


def is_object_file(fname):
    r = re.compile(r'\.(?P<extension>((so)|(a)|(o)))(\.|$)')
    return(check_regex(fname, r))


def search_directory(dname, token, type_check_fun, search_fun, r):
    contents = os.listdir(dname)
    for thing in contents:
        thing = os.path.join(dname, thing)
        if os.path.isfile(thing):
            if type_check_fun(thing):
                search_fun(thing, token)
        elif (r and os.path.isdir(thing)):
            search_directory(thing, token, type_check_fun, search_fun, r)


def search_main(name, token, type_check_fun, search_fun, r):
    if os.path.isfile(name):
        if type_check_fun(name):
            search_fun(name, token)
        else:
            raise TypeError("Incorrect file type.")
    elif os.path.isdir(name):
        search_directory(name, token, type_check_fun, search_fun, r)
    else:
        raise TypeError("Must be a directory or file.")


def object_main(name, token, r):
    search_main(name, token, is_object_file, nmsearch, r)


def source_main(name, token, r):
    search_main(name, token, is_c_source, catsearch, r)


def header_main(name, token, r):
    search_main(name, token, is_c_header, catsearch, r)


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
        raise Exception("Must select a mode of operation (-s, -o, -h, etc)")

    if o_mode:
        object_main(target, symbol, r)
    if s_mode:
        source_main(target, symbol, r)
    if h_mode:
        header_main(target, symbol, r)


if __name__ == '__main__':
    main()
